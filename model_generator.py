import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
from PIL import Image, ImageFile
import tensorflow as tf
import json
import glob
import random

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import gradio as gr
ImageFile.LOAD_TRUNCATED_IMAGES = True

# import datasets
import pathlib
dataset_path = "/content/drive/MyDrive/DLW/flood"
train_data_dir = pathlib.Path(dataset_path+"/images")
test_data_dir = pathlib.Path(dataset_path+"/images")

train_files = glob.glob(r''+dataset_path+"/train/images/*.png")
train_files = list(filter(lambda x: "post" in x, train_files))
train_files = random.sample(train_files, 1500)
# train_files = random.sample(train_files, 250)
train_datasize = len(train_files)
print("training data:", len(train_files))

test_files = glob.glob(r''+dataset_path+"/test/images/*.png")
test_files = list(filter(lambda x: "post" in x, test_files))
test_files = random.sample(test_files, 500)
# test_files = random.sample(test_files, 100)
test_datasize = len(test_files)
print("test data:", len(test_files))