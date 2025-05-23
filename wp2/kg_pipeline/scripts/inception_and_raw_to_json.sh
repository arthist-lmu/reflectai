#!/bin/bash

if [ ${#} -gt 4 ]
then
    python convert_inception.py -i ${1} -u ${2} -o ${3}
    python convert_raw_annotation_to_json.py -i ${4} -u ${2} -o ${5} -a ${3}
else
    python convert_raw_annotation_to_json.py -i ${1} -u ${2} -o ${3} -a ${4}
fi
