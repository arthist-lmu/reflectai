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
    parser = argparse.ArgumentParser(description="Knowledge extraction pipeline script")

    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-i", "--input_path", help="path to input file")
    parser.add_argument(
        "-u", "--user", help="only convert all annotations from a specific user"
    )
    parser.add_argument("-o", "--output_path", help="path to the output file")
    args = parser.parse_args()
    return args


def parse_xmi_file(root, tripplets):
    mapping = {}
    unique = set()

    text = load_text(root)
    for elem in root.iter():
        if 'ContentType' in elem.attrib.keys() or 'EntityType' in elem.attrib.keys():
            begin = int(elem.attrib['begin']) #- 1
            end = int(elem.attrib['end']) #+ 1 #because sometimes the object is not always fully grabbed
            if text is None:
                continue
            value = text[begin:end]
            key = elem.attrib['{http://www.omg.org/XMI}id']
            mapping.update({key: value})
        elif ('Dependent' in elem.attrib.keys() and 'Governor' in elem.attrib.keys() and
              'Relationship' in elem.attrib.keys()):
            s_code = elem.attrib['Governor']
            o_code = elem.attrib['Dependent']
            p = elem.attrib['Relationship']
            s = mapping.get(s_code)
            o = mapping.get(o_code)
            if p is not None and s is not None and o is not None:
                unique.add((s, p, o))

    for unique_tripplet in unique:
        tripplets = xmi_parse_helper(tripplets, unique_tripplet)

    return tripplets



def xmi_parse_helper(tripplets, tripplet):

    if tripplet[0] not in tripplets.keys():
        # add whole triplet
        entry = {tripplet[0]:{tripplet[1]: tripplet[2]}}
        tripplets.update(entry)
    else:
        if tripplet[1] not in tripplets[tripplet[0]]:
            # only add the predicate object pair for relevant subject
            tripplets[tripplet[0]].update({tripplet[1]: tripplet[2]})

        elif tripplet[2] not in tripplets[tripplet[0]][tripplet[1]]:
            # only add object to relevant predicate if not already present
            contents = tripplets[tripplet[0]][tripplet[1]]
            if type(contents) == list:
                contents.append(tripplet[2])
            else:
                contents = [contents, tripplet[2]]

            tripplets[tripplet[0]].update({tripplet[1]: contents})

    return tripplets


def load_text(root, annotations_path='./annotation'):
    for elem in root.iter():
        if 'documentTitle' in elem.attrib.keys():
            for annotation_texts in os.listdir(annotations_path):
                for annotation_text in os.listdir(annotations_path + '/' + annotation_texts):
                    if elem.attrib["documentTitle"] == annotation_text:
                        with open(annotations_path +'/' + annotation_texts +  f'/{annotation_text}', encoding='utf-8') as fp:
                            text = fp.read()

                        return text
                    


def extrext_annotation(zip_file_object, tripplets):
    data = None
    with ZipFile(zip_file_object) as zip_file:
        for x in zip_file.infolist():
            if re.match(r".*\.xmi", x.filename):
                with zip_file.open(x.filename) as f:
                    data = f.read()

    root = ET.fromstring(data)

    return parse_xmi_file(root, tripplets)



def annotationxmi_to_annotationjson():
    # transform annotation xmi file into annotation json file
    args = parse_args()
    with ZipFile(args.input_path) as zip_file:
        trips = {}
        for x in zip_file.infolist():
            if args.user:
                # print(r"annotation/*/" + args.user + "\.xml")
                if re.match(r"annotation/.*/" + args.user + "\.zip", x.filename):

                    #with open('./annotated_texts.txt', 'a', encoding='utf-8') as fp:
                    #    fp.write(x.filename[11:-14] + '\n')

                    with zip_file.open(x.filename) as f:
                        trips = extrext_annotation(BytesIO(f.read()), trips)
    """
    # ---------------------------------
    # this part only for individual xmi files
    trips = {}
    with open('tzischkin.xmi', 'r', encoding='utf-8') as fp:
        root = ET.fromstring(fp.read())
        trips = parse_xmi_file(root, trips)
    # ---------------------------------
    """

    if args.output_path:
        with open(args.output_path, 'w', encoding='utf-8') as fp:
            json.dump(trips, fp, indent=4, ensure_ascii=False)



def main():
    annotationxmi_to_annotationjson()

        
    return 0


if __name__ == "__main__":
    sys.exit(main())
