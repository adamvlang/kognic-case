from annotation_convertion.kognic_to_openlabel import convert
import json

path_to_kognic_annotation = 'kognic_1.json'
with open(path_to_kognic_annotation, 'r') as content:
    kognic_annotation = json.load(content)

open_label_annotation = convert(kognic_annotation)

print(open_label_annotation)