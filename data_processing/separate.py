import glob
import random
import sys
import os
from shutil import copy

_class = sys.argv[1]

image_path_list = []

image_path_list += sorted(glob.glob(os.path.join('./output/' + _class + "/", '*.jpg')))
random.shuffle(image_path_list)

num_images = len(image_path_list)

print("There are {} images for this class.".format(num_images))

train_set = image_path_list[:int(num_images*0.7)]
val_set = image_path_list[int(num_images*0.7): int(num_images*0.8)]
test_set = image_path_list[int(num_images*0.8):]


print("There are {} images for this train.".format(len(train_set)))
print("There are {} images for this val.".format(len(val_set)))
print("There are {} images for this test.".format(len(test_set)))

for pic in train_set:
    copy(pic, 'rgb_data/Train/' + _class)

for pic in val_set:
    copy(pic, 'rgb_data/Validation/' + _class)

for pic in test_set:
    copy(pic, 'rgb_data/Test/' + _class)
