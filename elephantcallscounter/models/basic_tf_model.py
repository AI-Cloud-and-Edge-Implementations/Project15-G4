import cv2
import os
import numpy as np
import tensorflow as tf


from tensorflow.keras import datasets, layers, models
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from sklearn.model_selection import train_test_split


def prepare_spectrograms():
    dest_directory = os.path.join(get_project_root(), 'data/spectrogram_images/training_data')
    os.mkdir(dest_directory)
    labels = []


def get_labels(dir_name):
    labels = []
    for file_name in os.listdir(dir_name):
        labels.append(int(file_name.split('_')[0]))

    return labels


def get_train_test_set(dir_path):
    labels = get_labels(dir_path)

    data = tf.keras.preprocessing.image_dataset_from_directory(
        dir_path,
        labels='inferred',
        label_mode = "int",
        class_names = None,
        color_mode = "rgb",
        batch_size = 32,
        shuffle = True,
        seed = None,
        image_size = (640, 480),
        interpolation = "bilinear",
        follow_links = False,
    )
    train_x, test_x, train_y, test_y = train_test_split(
        data, labels, test_size = 0.2
    )

    return train_x, test_x, train_y, test_y


def build_model():
    train_images, test_images, train_labels, test_labels = get_train_test_set(
        os.path.join(get_project_root(), 'data/spectrogram_bb/')
    )

    train_data = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
    valid_data = tf.data.Dataset.from_tensor_slices((test_images, test_labels))

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation = 'relu', input_shape = (480, 640, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation = 'relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation = 'relu'))
    model.summary()

    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation = 'relu'))
    model.add(layers.Dense(10))

    train_data = tf.expand_dims(train_data, axis = -1)

    model.compile(optimizer = 'adam',
                  loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
                  metrics = ['accuracy'])

    history = model.fit(
        train_data, epochs = 10,
        validation_data = valid_data
    )

    plt.plot(history.history['accuracy'], label = 'accuracy')
    plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc = 'lower right')

    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose = 2)

    print(test_acc)
