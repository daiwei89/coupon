import os
from os.path import dirname
from os.path import join
import pandas as pd
import collections
import sys
from util import *
from sklearn.feature_extraction import DictVectorizer as DV
import numpy as np
import itertools
import random

project_dir = dirname(dirname(os.path.realpath(__file__)))
data_dir = join(project_dir, 'data')

libfm_train = join(data_dir, 'pair_train.libfm')

out1 = join(data_dir, 'pair_train_train.libfm')
out2 = join(data_dir, 'pair_train_valid.libfm')

split1 = 0.8

if __name__ == "__main__":
  lines = open(libfm_train).readlines()
  random.shuffle(lines)
  num_lines_out1 = int(len(lines) * 0.8)
  open(out1, 'w').writelines(lines[:num_lines_out1])
  open(out2, 'w').writelines(lines[num_lines_out1:])
