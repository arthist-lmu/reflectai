import os
import sys
import re
import json
from io import BytesIO
import argparse
from typing import List, Dict
from tqdm import tqdm
import hashlib
from zipfile import ZipFile
import xml.etree.ElementTree as ET


def parse_args():
    parser = argparse.ArgumentParser(description="Script to extract the annotations of a specific user")

    parser.add_argument("-i", "--input_path", help="path to input file", required=True)
    parser.add_argument(
        "-u", "--user", help="only convert all annotations from a specific user", required=True
    )
    parser.add_argument("-o", "--output_path", help="path to the output directory", required=True)
    args = parser.parse_args()
    return args


def parse_xmi_file(root, tripplets, args):
    mapping = {}
    unique = set()

    #text = load_text(root)
    text = load_text2(root, args)
    for elem in root.iter():
        if 'ContentType' in elem.attrib.keys() or 'EntityType' in elem.attrib.keys():
            class_name = elem.attrib[list(elem.attrib.keys())[-1]]
            class_name = ''.join(x for x in class_name.title() if not x.isspace())
            begin = int(elem.attrib['begin']) 
            end = int(elem.attrib['end']) 
            if text is None:
                continue
            value = text[begin:end]
            key = elem.attrib['{http://www.omg.org/XMI}id']
                
            mapping.update({key: [value, class_name]})
        elif ('Dependent' in elem.attrib.keys() and 'Governor' in elem.attrib.keys() and
              'Relationship' in elem.attrib.keys()):
            s_code = elem.attrib['Governor']
            o_code = elem.attrib['Dependent']
            p = elem.attrib['Relationship']
            s_ = mapping.get(s_code)
            o_ = mapping.get(o_code)
            
            if p is not None and s_ is not None and o_ is not None:
                s = s_[0]
                o = o_[0]
                s_class_name = s_[1]
                o_class_name = o_[1]
                unique.add((s, p, o, s_class_name, o_class_name))

    for unique_tripplet in unique:
        tripplets = xmi_parse_helper(tripplets, unique_tripplet)

    return tripplets


def xmi_parse_helper(tripplets, tripplet):
    if tripplet[0] not in tripplets.keys():
        # add whole triplet. Also include class names of subject and object
        entry = {tripplet[0]:{tripplet[1]: [tripplet[2], {'o_class_name':tripplet[4]}], 's_class_name':tripplet[3]}}
        tripplets.update(entry)
    else:
        if tripplet[1] not in tripplets[tripplet[0]]:
            # only add the predicate object pair for relevant subject. THe object class names need to be properly included
            tripplets[tripplet[0]].update({tripplet[1]: [tripplet[2], {'o_class_name':tripplet[4]}]})

        elif tripplet[2] not in tripplets[tripplet[0]][tripplet[1]]:
            # only add object to relevant predicate if not already present. once again the object class names need to be included
            contents = tripplets[tripplet[0]][tripplet[1]][0]
            if type(contents) == list:
                contents.append(tripplet[2])
            else:
                contents = [contents, tripplet[2]]

            o_class_names =  tripplets[tripplet[0]][tripplet[1]][1]['o_class_name']
            if type(o_class_names) == list:
                o_class_names.append(tripplet[4])
            else:
                o_class_names = [o_class_names, tripplet[4]]

            tripplets[tripplet[0]].update({tripplet[1]: [contents, {'o_class_name':o_class_names}]})


    return tripplets


def load_text(root, annotations_path='/nfs/data/reflectai/data/annotation'):
    for elem in root.iter():
        if 'documentTitle' in elem.attrib.keys():
            for annotation_texts in os.listdir(annotations_path):
                for annotation_text in os.listdir(annotations_path + '/' + annotation_texts):
                    if elem.attrib["documentTitle"] == annotation_text:
                        with open(annotations_path +'/' + annotation_texts +  f'/{annotation_text}', encoding='utf-8') as fp:
                            text = fp.read()

                        return text
                    

def load_text2(root, args, annotations_path='/nfs/data/reflectai/data/annotation/txt/'):
    for elem in root.iter():
        if 'documentTitle' in elem.attrib.keys():
            for annotation_texts in os.listdir(annotations_path):
                if annotation_texts == elem.attrib["documentTitle"]:
                    with open(f'{annotations_path}/{annotation_texts}/{args.user}.txt', 'r', encoding='utf-8') as fp:
                        text = fp.read()

                    return text



def extrext_annotation(zip_file_object, tripplets, args):
    data = None
    with ZipFile(zip_file_object) as zip_file:
        for x in zip_file.infolist():
            if re.match(r".*\.xmi", x.filename):
                with zip_file.open(x.filename) as f:
                    data = f.read()

    root = ET.fromstring(data)

    return parse_xmi_file(root, tripplets, args)



def annotationxmi_to_annotationjson(save_individually):
    # transform annotation xmi file into annotation json file

    args = parse_args()
    with ZipFile(args.input_path) as zip_file:
        trips = {}
        for x in zip_file.infolist():
            if args.user:
                if re.match(r"annotation/.*/" + args.user + "\.zip", x.filename):
                    with zip_file.open(x.filename) as f:
                        trips = extrext_annotation(BytesIO(f.read()), trips, args)
                        if save_individually:
                            end = re.search('.*\.txt/', x.filename).span()[1]
                            with open(f'{args.output_path}/{x.filename[11:(end - 5)]}.json', 'w', encoding='utf-8') as fp:
                                json.dump(trips, fp, indent=4, ensure_ascii=False)
                            trips = {}
    """
    # ---------------------------------
    # this part only for individual xmi files
    trips = {}
    with open('Conversion.xmi', 'r', encoding='utf-8') as fp:
        root = ET.fromstring(fp.read())
        trips = parse_xmi_file(root, trips, args)
    # ---------------------------------
    """
    if not save_individually:
        with open(f'./annotated_tripplets_of_{args.user}.json', 'w', encoding='utf-8') as fp:
            json.dump(trips, fp, indent=4, ensure_ascii=False)



def main():
    # toggle True to False if you want to gather all the annotations into one big json file rather than 
    # many individual ones for each painting
    annotationxmi_to_annotationjson(True)
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
