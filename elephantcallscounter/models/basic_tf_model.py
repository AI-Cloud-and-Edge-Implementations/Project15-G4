import os

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow import keras

import tensorflow as tf

import matplotlib.pyplot as plt

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


def get_train_test_set(dir_path):
    # create generator
    datagen = ImageDataGenerator()
    # prepare an iterators for each dataset
    train_it = datagen.flow_from_directory(join_paths([dir_path, 'train']), target_size = (224, 224), class_mode = 'categorical')
    val_it = datagen.flow_from_directory(join_paths([dir_path, 'valid']), target_size = (224, 224), class_mode = 'categorical')
    test_it = datagen.flow_from_directory(join_paths([dir_path, 'test']), target_size = (224, 224), class_mode = 'categorical')
    return train_it, val_it, test_it


def model_layers():
    model = Sequential()

    model.add(Conv2D(16, kernel_size = (3, 3), activation = 'relu',
                     input_shape = (150, 150, 3)))
    model.add(MaxPooling2D(pool_size = (2, 2)))

    model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))

    model.add(Conv2D(128, kernel_size = (3, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))

    model.add(Flatten())
    model.add(Dense(512, activation = 'relu'))
    model.add(Dense(3, activation = 'sigmoid'))


def build_model():
    train_it, val_it, test_it = get_train_test_set(
        os.path.join(get_project_root(), 'data/spectrogram_bb/')
    )

    batch_size = 32

    input_t = keras.Input(shape=(224, 224, 3))
    res_model = keras.applications.ResNet50(include_top=False,weights="imagenet",input_tensor=input_t)

    for layer in res_model.layers[:143]:
        layer.trainable = False
    # Check the freezed was done ok
    for i, layer in enumerate(res_model.layers):
        print(i, layer.name, "-", layer.trainable)

    to_res = (224, 224)

    model = keras.models.Sequential()
    to_res = (224, 224)
    model.add(keras.layers.Lambda(lambda image: tf.image.resize(image, to_res)))
    model.add(res_model)
    model.add(keras.layers.Flatten())
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(256, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=keras.optimizers.RMSprop(lr=2e-5),
                  metrics=['accuracy'])

    history = model.fit(train_it, epochs=20, validation_data=val_it, batch_size=batch_size)

    plt.plot(history.history['accuracy'], label = 'accuracy')
    plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc = 'lower right')

    test_loss, test_acc = model.evaluate(test_it, verbose = 2)

    print(test_acc)
