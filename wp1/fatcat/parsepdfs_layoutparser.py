from functools import partial
import itertools
import json
import os
from pathlib import Path

import click
import layoutparser as lp
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pdf2image
import pycountry
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
from transformers import pipeline, Pipeline


def pdf_to_image(fpath: Path) -> Image:
    images = pdf2image.convert_from_bytes(fpath.read_bytes())
    return images


def parse_image(model: lp.models.base_layoutmodel.BaseLayoutModel, lang_pipeline: Pipeline, image: Image):
    image = np.array(image)
    layout = model.detect(image)

    layout = filter_overlapping(layout)
    text_blocks, figure_blocks = get_text_figure_blocks(layout)
    if len(text_blocks) == 0:
        return

    lang = detect_language(lang_pipeline, image, text_blocks[:5])

    for block in text_blocks:
        ocr_text_block(image, block, lang)

    if len(figure_blocks) > 0:
        figures_captioned, text_blocks = find_captions(figure_blocks, text_blocks)

    if len(text_blocks) > 0:
        text_blocks = order_text(text_blocks, image)
        return {'content': ' '.join(text_blocks.get_texts()), 'language': lang}

    return None


def get_text_figure_blocks(layout: lp.Layout):
    text_blocks = lp.Layout([b for b in layout if b.type == 'Text' or b.type == 'Title'])
    figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])
    text_blocks = lp.Layout([
        b for b in text_blocks
        if not any(b.is_in(b_fig)
        for b_fig in figure_blocks)
    ])
    return text_blocks, figure_blocks


def order_text(layout: lp.Layout, image: Image):
    _, w = image.shape[:2]

    column_layout = []
    for block in layout:
        if block.width > ((w - 200) / 2):
            column_layout.append(1)
        elif block.width > ((w - 200) / 3):
            column_layout.append(2)
        else:
            column_layout.append(3)
    column_layout = min(column_layout)

    if column_layout == 1:
        blocks = sorted(layout, key=lambda b: b.coordinates[1])
    elif column_layout == 2:
        left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(image)
        left_blocks = sorted(
            layout.filter_by(left_interval, center=True),
            key=lambda b: b.coordinates[1]
        )
        right_blocks = sorted(
            [b for b in layout if b not in left_blocks],
            key=lambda b: b.coordinates[1]
        )
        blocks = left_blocks + right_blocks
    else:
        left_interval = lp.Interval(0, w/2, axis='x').put_on_canvas(image)
        left_blocks = sorted(
            layout.filter_by(left_interval, center=True),
            key=lambda b: b.coordinates[1]
        )
        middle_interval = lp.Interval(w/4, w*0.75, axis='x').put_on_canvas(image)
        middle_blocks = sorted(
            layout.filter_by(middle_interval, center=True),
            key=lambda b: b.coordinates[1]
        )
        right_blocks = sorted(
            [b for b in layout if b not in left_blocks and b not in middle_blocks],
            key=lambda b: b.coordinates[1]
        )
        blocks = left_blocks + middle_blocks + right_blocks

    text_blocks = lp.Layout([
        b.set(id = idx)
        for idx, b in enumerate(blocks)
    ])
    return text_blocks


def filter_overlapping(layout: lp.Layout, threshold: float = 0.7):
    duplicates = []
    for b1, b2 in itertools.combinations(layout, 2):
        size1 = b1.width * b1.height
        size2 = b2.width * b2.height
        intersection = b1.intersect(b2)
        inter_size = intersection.width * intersection.height
        if inter_size > size1 * threshold or inter_size > size2 * threshold:
            if size1 > size2:
                duplicates.append(b2)
            else:
                duplicates.append(b1)
    return lp.Layout([b for b in layout if b not in duplicates])


def find_captions(figure_blocks: lp.Layout, text_blocks: lp.Layout):
    potential_captions = [
        text_block
        for text_block in text_blocks
        if text_block.text.strip().startswith('Fig')
    ]
    figures = []
    captions = set()
    for figure in figure_blocks:
        for caption in potential_captions:
            dist1 = caption.coordinates[1] - figure.coordinates[3]
            dist2 = figure.coordinates[1] - caption.coordinates[3]
            dist3 = caption.coordinates[0] - figure.coordinates[2]
            dist4 = figure.coordinates[0] - caption.coordinates[2]
            min_dist = min([d for d in (dist1, dist2, dist3, dist4) if d > 0])
            if min_dist > 0 and min_dist < 80:
                figures.append((figure, caption))
                captions.add(id(caption))
                break
    text_blocks = lp.Layout([b for b in text_blocks if id(b) not in captions])
    return figures, text_blocks


def visualize_detected_layout(image: Image, layout: lp.Layout):
    # pillow 9.5.0 needed for show_element_id
    image = lp.draw_box(image, layout, box_width=10, show_element_id=True)
    plt.imshow(image)
    plt.show()


def ocr_text_block(image, block, lang='en'):
    lang = pycountry.languages.get(alpha_2=lang).alpha_3
    ocr_agent = lp.TesseractAgent(languages=lang)
    segment_image = (block.pad(left=5, right=5, top=5, bottom=5)
                          .crop_image(image))
    text = ocr_agent.detect(segment_image)
    block.set(text=text, inplace=True)
    return text


def detect_language(pipeline: Pipeline, image: Image, text_blocks: lp.Layout):
    # Language packs need to be installed via the OS package manager.
    # They are called something like tesseract-lang-spa or tesseract-ocr-all.
    text = ' '.join([ocr_text_block(image, block) for block in text_blocks])
    return pipeline(text, truncation=True, max_length=128)[0]['label']


@click.command()
@click.option('--input', required=True, help='Input pdf or folder with pdfs',
              type=click.Path(dir_okay=True, readable=True, path_type=Path, exists=True))
@click.option('--output', default=Path('parsedpdfs.jsonl'), help='Output file',
              type=click.Path(writable=True, dir_okay=False, path_type=Path))
@click.option('--outputprogress', default=Path('parsedpdfs_progress.jsonl'), help='Output progress file',
              type=click.Path(writable=True, dir_okay=False, path_type=Path))
@click.option('--cpu', default=False, help='Run on CPU not CUDA', is_flag=True)
def main(input: Path, output: Path, outputprogress: Path, cpu: bool):
    if input.is_file():
        files = [input]
    else:
        files = list(input.rglob('*pdf'))

    # There is some mess-up between the model URL having "&dl=1" at the end
    # and Detectron not accepting that.
    if not os.path.exists(os.path.expanduser('~/.torch/iopath_cache/s/dgy9c10wykk4lq4/model_final.pth')):
        try:
            lp.models.Detectron2LayoutModel(config_path='lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config')
        except AssertionError:
            pass
    if os.path.exists(os.path.expanduser('~/.torch/iopath_cache/s/dgy9c10wykk4lq4/model_final.pth?dl=1')):
        os.rename(os.path.expanduser('~/.torch/iopath_cache/s/dgy9c10wykk4lq4/model_final.pth?dl=1'),
                  os.path.expanduser('~/.torch/iopath_cache/s/dgy9c10wykk4lq4/model_final.pth'))
    model = lp.models.Detectron2LayoutModel(
        config_path = 'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
        label_map = {0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
        extra_config = ["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.6],  # probability when text block is detected as such
        model_path = os.path.expanduser('~/.torch/iopath_cache/s/dgy9c10wykk4lq4/model_final.pth')
    )

    device = 'cuda'
    if cpu:
        device = 'cpu'
    lang_detect_model = "papluca/xlm-roberta-base-language-detection"
    lang_detect_pipeline = pipeline("text-classification", model=lang_detect_model, device=device)

    if outputprogress.exists():
        with outputprogress.open() as f:
            progress = [l.strip() for l in f.readlines()]
    else:
        progress = []

    with output.open('a') as f, outputprogress.open('a') as f_progress:
        for file in tqdm(files):
            if file.name in progress:
                continue
            images = pdf_to_image(file)
            texts = []

            texts = [
                text
                for text in thread_map(partial(parse_image, model, lang_detect_pipeline),
                                       images,
                                       max_workers=20,
                                       leave=True)
            ]

            f.write(json.dumps({'id': file.name, 'text': texts}) + '\n')

            progress.append(file.name)
            f_progress.write(file.name + '\n')


if __name__ == '__main__':
    main()
