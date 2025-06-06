import os
import json
import jsonl
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Script to convert text inputs to jsonl files. Optionally also includes the Ground Truth annotations as a json-dictionary.")

    parser.add_argument("-i", "--input_path",  help="path to input files", required=True)
    parser.add_argument("-o", "--output_path", help="path to the output file", required=True)
    parser.add_argument("-u", "--user", help="The Textfile the specified user used for annotations", required=True)
    parser.add_argument("-a", "--annotations", help="path to the annotations file's directory")

    args = parser.parse_args()
    return args


def create_jsonl_file():

    args = parse_args()
    collection = []
    # if used with annotations make sure that only the textes are given that have the annotations

    # /nfs/data/reflectai/data/annotation/txt/
    for annotations_texts in os.listdir(args.input_path):
        user = args.user
        if args.user == 'curation':
            user = 'INITIAL_CAS'
        try:
            with open(f'{args.input_path}/{annotations_texts}/{user}.txt', encoding='utf-8') as fp:
                annotations = {}
                if args.annotations:
                    # not all the txt files have been annotated/curated
                    with open(f'{args.annotations}/{annotations_texts[:-4]}.json', 'r', encoding='utf-8') as f:
                        annotations = json.load(f)
                    
                
                read = fp.read()
                text = {'text': [{'content': read}], 'id': annotations_texts, 'annotations':annotations}
                collection.append(text)
        except FileNotFoundError:
            continue

    # "/nfs/home/ritterd/reflect/reflectai/wp2/test/gollie_testset/gollietestset.jsonl"
    jsonl.dump(collection, args.output_path)
            
            

if __name__ == '__main__':
    create_jsonl_file()
