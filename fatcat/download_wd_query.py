import csv
import os
import logging
import requests


logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', filename='download.log', encoding='utf-8', level=logging.INFO)

with open(os.path.join( os.getcwd(), 'wd_query_list_download_links.csv' )) as csvfile:
    csvreader = csv.reader(csvfile)
    for i, row in enumerate(csvreader):
        filename = row[0] + ".pdf"
        logging.info("Processing line: " + str(i) + " with this filename: " + str(filename) + " with this link: " + row[5])
        if os.path.exists(filename):
            logging.info("file already downloaded, skipping")
        else:
            logging.info("Starting download on line " + str(i))
            try:
                paper = requests.get(row[5])
                open(filename, 'wb').write(paper.content)
            except:
                logging.error("Download failed on line: " + str(i))
        if i > 5:
            break
logging.info("Finished download")
