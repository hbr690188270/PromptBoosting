import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.template import SentenceTemplate, TemplateSaver
from src.utils import ROOT_DIR
import json

dataset = "mr"
generated_file_path = 'templates/raw_t5_generated_sorted_{dataset}.txt'
# dataset = "imdb"

saver = TemplateSaver(template_path = ROOT_DIR + f'templates/t5_sorted_{dataset}/')

raw_list = []
with open(ROOT_DIR + generated_file_path, 'r', encoding = 'utf-8') as f:
    for line in f:
        raw_list.append(line.strip()[6:-6])

curr_idx = saver.num_templates
def transform_raw(raw_template, idx,saver):
    items = raw_template.split("*")
    name = f"{dataset}_t5_sorted_template{idx+1}"
    json_list = []
    segment_id = 1
    for i, item in enumerate(items):
        if 'sent_0' in item:
            desc_dict = {"meta": "text_a"}
        elif 'sent_1' in item:
            desc_dict = {"meta": "text_b"}
        elif item == 'mask':
            desc_dict = {"meta": "output_token"}
        else:
            content = item.replace("_"," ")
            desc_dict = {"meta": f"prompt_segment{segment_id}", "content": content}
            segment_id += 1
        json_list.append(desc_dict)
    json_dict = {"name": name, "template": json_list}
    with open(saver.template_path + f'{name}.json', 'w', encoding = 'utf-8') as f:
        json.dump(json_dict, f, indent = 4)

for raw_template in raw_list[:10]:
    transform_raw(raw_template, curr_idx, saver)
    curr_idx += 1

