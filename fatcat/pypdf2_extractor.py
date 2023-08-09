import fitz
import os
import json
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename='download.log', encoding='utf-8', level=logging.INFO)


def pdf_to_json_and_images(pdf_path, processed_path):
    document = fitz.open(pdf_path)
    num_pages = document.page_count
    text_per_page = []
    images = []

    archiveorg_id = os.path.basename(pdf_path).replace('.pdf', '')

    pdf_folder = os.path.join(processed_path, archiveorg_id)
    os.makedirs(pdf_folder, exist_ok=True)

    for page_num in range(num_pages):
        page = document.load_page(page_num)
        text_per_page.append(page.get_text())

        page_width, page_height = page.rect.width, page.rect.height

        for img_index in page.get_images(full=True):
            xref = img_index[0]
            base_image = document.extract_image(xref)
            if isinstance(base_image, dict):
                image_bytes = base_image["image"]

                image_width, image_height = base_image["width"], base_image["height"]
                
                #if archiveorg_id == "7eax5yimbneurdhsirrv5rdcjq":
                #    print("Page width: " +  str(page_width) + " image width: " + str(image_width))
                #    print("Page height: " +  str(page_height) + " image height: " + str(image_height))
                
                #if image_width != page_width or image_height != page_height:
                image_filename = os.path.join(pdf_folder, f'image{page_num}_{img_index[0]}.png')
                with open(image_filename, 'wb') as image_file:
                    image_file.write(image_bytes)

                images.append({
                    'id': img_index[0],
                    'page': page_num,
                    'path': image_filename
                })

    json_content = {
        'archiveorg_id': archiveorg_id,
        'pages': text_per_page,
        'images': images
    }

    json_filename = os.path.join(pdf_folder, f'{archiveorg_id}.json')

    with open(json_filename, 'w') as json_file:
        json.dump(json_content, json_file, ensure_ascii=False, indent=4)

    print(f'Text content and images from {pdf_path} have been successfully written to {pdf_folder}')

folder_path = '/nfs/data/reflectai/scientific_pdfs'

total_pdfs = sum([filename.endswith('.pdf') for filename in os.listdir(folder_path)])

processed_path = os.path.join(folder_path, 'processed')
os.makedirs(processed_path, exist_ok=True)

processed_count = 0
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(folder_path, filename)
        pdf_to_json_and_images(pdf_path, processed_path)
        
        processed_count += 1
        percentage_done = (processed_count / total_pdfs) * 100
        logging.info(f'Processed {processed_count} out of {total_pdfs} PDFs ({percentage_done:.2f}% done)')

print('All PDF files have been converted to JSON, and images have been extracted.')

