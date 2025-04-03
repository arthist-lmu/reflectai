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


def extrext_text(data):
    pass


def extrext_annotation(zip_file_object):
    data = None
    with ZipFile(zip_file_object) as zip_file:
        for x in zip_file.infolist():
            if re.match(r".*\.xmi", x.filename):
                with zip_file.open(x.filename) as f:
                    data = f.read()

    root = ET.fromstring(data)
    for elem in root.iter():
        print(elem.tag)

    # print("####")
    # for elem in root.findall(
    #     ".//de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence/"
    # ):
    #     for x in elem:
    #         if x.tag == "webanno.custom.Namedentity":
    #             data = {
    #                 "begin": x.attrib.get("begin"),
    #                 "end": x.attrib.get("end"),
    #                 "type": x.attrib.get("EntityType"),
    #             }
    #             print(data)

    #         if x.tag == "custom.Span":
    #             print("+++++++++++++++++++++++++++++++++++++++")
    #         if x.tag == "custom.Relation":
    #             print("+++++++++++++++++++++++++++++++++++++++")


def main():
    args = parse_args()

    with ZipFile(args.input_path) as zip_file:

        for x in zip_file.infolist():
            should_read = False
            if args.user:
                # print(r"annotation/*/" + args.user + "\.xml")
                if re.match(r"annotation/.*/" + args.user + "\.zip", x.filename):
                    should_read = True
                    with zip_file.open(x.filename) as f:
                        extrext_annotation(BytesIO(f.read()))

            if should_read:
                print(x)
                # with zip_file.open(x.filename) as f:
                #     print("#############################################")
                #     print(x.filename)
                #     print("#############################################")
                #     print(extrext_annotation(f.read()))
                # exit()

            # print(x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
