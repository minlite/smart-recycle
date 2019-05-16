"""
ECE196 Face Recognition Project
Author: W Chen

Use this as a template to:
1. load weights for vgg16
2. load images
3. finetune network
4. save weights
"""

from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras import optimizers
from keras.layers import Dropout, Flatten, Dense
from keras.utils.np_utils import to_categorical
from keras.optimizers import SGD
import numpy as np
import glob
import os
import cv2
import random

IMG_H, IMG_W, NUM_CHANNELS = 224, 224, 3
#MEAN_PIXEL = np.array([104., 117., 123.]).reshape((1, 1, 3))
TRAIN_DIR = './data/Train'  # TODO
VAL_DIR = './dataValidation'  # TODO
NUM_EPOCHS = 7  # TODO
BATCH_SIZE = 16
NUM_CLASSES = 2  # TODO


def load_model():
    # TODO: use VGG16 to load lower layers of vgg16 network and declare it as base_model
    base_model = VGG16(include_top=False,weights = 'imagenet',input_shape = (IMG_H, IMG_W, NUM_CHANNELS))
    # TODO: use 'imagenet' for weights, include_top=False, (IMG_H, IMG_W, NUM_CHANNELS) for input_shape

    print('Model weights loaded.')
    base_out = base_model.output
    # TODO: add a flatten layer, a dense layer with 256 units, a dropout layer with 0.5 rate,
    x = Flatten()(base_out)
    x = Dense(256, activation='relu')(x)
    x = Dropout(.5)(x)
    
    # TODO: and another dense layer for output. The final layer should have the same number of units as classes
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    print 'Build model'
    model.summary()

    # TODO: compile the model, use SGD(lr=1e-4,momentum=0.9) for optimizer, 'categorical_crossentropy' for loss,
    model.compile(optimizer=SGD(lr=1e-4,momentum=0.9), loss='categorical_crossentropy',metrics=['accuracy'])
    # TODO: and ['accuracy'] for metrics

    print 'Compile model'
    return model


def load_data(src_path):
    # under train/val/test dirs, each class is a folder with numerical numbers
    # X: number_images * height * width * channels
    # Y: number_images * 1
    class_path_list = sorted(glob.glob(os.path.join(src_path, '*')))
    image_path_list = []
    for class_path in class_path_list:
        image_path_list += sorted(glob.glob(os.path.join(class_path, '*jpg')))
    random.shuffle(image_path_list)
    num_images = len(image_path_list)
    print '-- This set has {} images.'.format(num_images)
    X = np.zeros((num_images, IMG_H, IMG_W, NUM_CHANNELS))
    Y = np.zeros((num_images, 1))
    # read images and labels
    for i in range(num_images):
        image_path = image_path_list[i]
        label = int(image_path.split('/')[-2])
        image = cv2.imread(image_path, 1)
        image = cv2.resize(image, (IMG_H, IMG_W))
        X[i, :, :, :] = image
        Y[i, :] = label
    Y = to_categorical(Y, NUM_CLASSES)
    return X, Y


def main():
    # make model
    model = load_model()
    print 'VGG16 created\n'

    # read train and validation data and train the model for n epochs
    print 'Load train data:'
    X_train, Y_train = load_data(TRAIN_DIR)
    print 'Load val data:'
    X_val, Y_val = load_data(VAL_DIR)
    # TODO: Train model
    model.fit(x=X_train, y=Y_train, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS, validation_data=(X_val,Y_val))
    # TODO: Save model weights
    model.save('./vgg16_new_version_weights.h5')
    print 'model weights saved.'
    return


if __name__ == '__main__':
    main()
