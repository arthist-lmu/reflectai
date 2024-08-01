from pathlib import Path

import imageio
import layoutparser as lp
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pdf2image
from tqdm import tqdm


def pdf_to_image(fpath: Path) -> Image:
    images = pdf2image.convert_from_bytes(fpath.read_bytes())
    return images


def parse_image(model: lp.models.base_layoutmodel.BaseLayoutModel, image: Image):
    image = np.array(image)
    layout = model.detect(image)

    # separate text and figure blocks
    text_blocks = lp.Layout([b for b in layout if b.type == 'Text' or b.type == 'Title'])
    figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])
    text_blocks = lp.Layout([
        b for b in text_blocks
        if not any(b.is_in(b_fig) 
        for b_fig in figure_blocks)
    ])

    # set order of text blocks
    h, w = image.shape[:2]
    left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(image)
    left_blocks = sorted(
        text_blocks.filter_by(left_interval, center=True),
        key=lambda b: b.coordinates[1]
    )
    right_blocks = sorted(
        [b for b in text_blocks if b not in left_blocks],
        key=lambda b: b.coordinates[1]
    )
    text_blocks = lp.Layout([
        b.set(id = idx) 
        for idx, b in enumerate(left_blocks + right_blocks)
    ])

    # run OCR
    for block in text_blocks:
        text = ocr_text_block(image, block)
        print(text)


def visualize_detected_layout(image: Image, layout: lp.Layout):
    image = lp.draw_box(image, layout, box_width=10)
    plt.imshow(image)
    plt.show()


def ocr_text_block(image, block, lang='eng'):
    ocr_agent = lp.TesseractAgent(languages=lang)
    segment_image = (block.pad(left=5, right=5, top=5, bottom=5)
                          .crop_image(image))
    text = ocr_agent.detect(segment_image)
    block.set(text=text, inplace=True)
    return text


def main(path: Path):
    if path.is_file():
        files = [path]
    else:
        files = path.rglob('*pdf')

    model = lp.models.Detectron2LayoutModel(
        config_path = 'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
        label_map = {0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
        extra_config = ["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.6]  # probability when text block is detected as such
    )

    for file in tqdm(files):
        images = pdf_to_image(file)

        for image in tqdm(images):
            parse_image(model, image)


if __name__ == '__main__':
    main(Path('/nfs/data/reflectai/scientific_pdfs'))
