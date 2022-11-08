import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from src.utils import ROOT_DIR
import datasets
import pandas as pd

ag_dataset = datasets.load_dataset("ag_news", cache_dir = ROOT_DIR + 'dataset_cache/ag_news/')
train_dataset = ag_dataset['train']
test_dataset = ag_dataset['test']

output_dir = ROOT_DIR + 'datasets/original/ag_news/'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
pd_train = train_dataset.to_pandas()
pd_train.to_csv(output_dir + 'train.csv')
pd_test = test_dataset.to_pandas()
pd_test.to_csv(output_dir + 'test.csv')

