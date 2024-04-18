import layoutparser as lp
import numpy as np
import pdf2image
import imageio
import matplotlib.pyplot as plt

images = pdf2image.convert_from_bytes(open('/home/kristbaum/Projects/redai-data/fatcat/1467-8365.12629.pdf', 'rb').read())
#image = np.array(image)
model = lp.Detectron2LayoutModel(
            config_path ='lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config', # In model catalog
            label_map   ={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"}, # In model`label_map`
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8] # Optional
        )

for image in images:
    #ocr_agent = lp.ocr.TesseractAgent()
    
    image = np.array(image)
    
    layout = model.detect(image)
    print(layout)

    for i, block in enumerate(layout.to_dict()['blocks']):
        image_part = image[int(block['y_1']):int(block['y_2']), int(block['x_1']):int(block['x_2'])]
        imageio.imgwrite('./output_image{i}.jpg')
        
        plt.imshow(image)

#model.detect(image)