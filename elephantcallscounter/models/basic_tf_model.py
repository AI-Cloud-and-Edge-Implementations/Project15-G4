import os
import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

from elephantcallscounter.utils.path_utils import get_project_root


def prepare_spectrograms():
    dest_directory = os.path.join(get_project_root(), 'data/spectrogram_images/training_data')
    os.mkdir(dest_directory)
    labels = []


def get_train_test_set():
    train_images = []
    img_height = 480
    img_width = 640
    batch_size = 32
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        os.path.join(get_project_root(), 'data/spectrogram_images/CroppedTrainingSet/nn03d'),
        validation_split = 0.2,
        subset = "training",
        seed = 123,
        image_size = (img_height, img_width),
        batch_size = batch_size
    )

    return train_ds


def build_model():
    train_images, test_images, train_labels, test_labels = get_train_test_set()

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation = 'relu', input_shape = (32, 32, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation = 'relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation = 'relu'))
    model.summary()

    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation = 'relu'))
    model.add(layers.Dense(10))

    model.compile(optimizer = 'adam',
                  loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
                  metrics = ['accuracy'])

    history = model.fit(
        train_images, train_labels, epochs = 10,
        validation_data = (test_images, test_labels)
    )

    plt.plot(history.history['accuracy'], label = 'accuracy')
    plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc = 'lower right')

    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose = 2)

    print(test_acc)
