import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.template import SentenceTemplate, TemplateSaver
from src.utils import ROOT_DIR
from src.data_util import dataset_transform
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type = str, default = 'sst', choices = [
    'sst', 'sst-5', 'mr', 'cr', 'mpqa','subj','trec', 'agnews', 'cola', 'mnli', 'snli', 'qnli', 'rte', 'mrpc','qqp'
], help = "indicate the dataset name, please use lower-cased characters"
)
parser.add_argument("--raw_template_path", type = str, help = "the path to the prompt file generated by LM-BFF")
parser.add_argument("--lm_type", type = str, default = 'mlm', choices = ['mlm','causal'], help = "the type of pre-trained language model")
parser.add_argument("--required_num", type = int, default = 10, help = "How many templates you want to extract from the raw file to the standard json format")
parser.add_argument("--start_idx", type = int, default = 0, help = "where to start extracting")

args = parser.parse_args()

dataset = args.dataset
raw_template_path = args.raw_template_path
lm_type = args.lm_type

if lm_type == 'mlm':
    saver = TemplateSaver(template_path = os.path.join(ROOT_DIR, f'templates/t5_sorted_{dataset}/'))
elif lm_type == 'causal':
    saver = TemplateSaver(template_path = os.path.join(ROOT_DIR, f'templates/causal_lm_t5_sorted_{dataset}/'))
else:
    raise NotImplementedError

raw_list = []
with open(os.path.join(ROOT_DIR, raw_template_path), 'r', encoding = 'utf-8') as f:
    for line in f:
        if line.strip()[-7:] == '**sep+*':
            raw_list.append(line.strip()[6:-7])
        elif line.strip()[-6:] == '*sep+*':
            raw_list.append(line.strip()[6:-6])
        else:
            raise NotImplementedError

curr_idx = saver.num_templates
def transform_raw(raw_template, idx,saver):
    items = raw_template.split("*")
    if lm_type == 'mlm':
        name = f"{dataset}_t5_sorted_template{idx+1}"
    elif lm_type == 'causal':
        name = f"{dataset}_t5_sorted_causal_lm_template{idx+1}"
    else:
        raise NotImplementedError
    json_list = []
    segment_id = 1
    for i, item in enumerate(items):
        if 'sent_0' in item or 'sent-_0' in item:
            desc_dict = {"meta": "text_a"}
        elif 'sent_1' in item or '+sentl_1' in item:
            desc_dict = {"meta": "text_b"}
        elif item == 'mask':
            if lm_type == 'mlm':
                desc_dict = {"meta": "output_token"}
            else:
                continue
        else:
            content = item.replace("_"," ")
            desc_dict = {"meta": f"prompt_segment{segment_id}", "content": content}
            segment_id += 1
        json_list.append(desc_dict)
    json_dict = {"name": name, "template": json_list}
    with open(saver.template_path + f'{name}.json', 'w', encoding = 'utf-8') as f:
        json.dump(json_dict, f, indent = 4)

for raw_template in raw_list[args.start_idx:args.start_idx + args.required_num]:
    transform_raw(raw_template, curr_idx, saver)
    curr_idx += 1

