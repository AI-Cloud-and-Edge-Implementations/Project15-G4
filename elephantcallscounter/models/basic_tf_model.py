import cv2
import os
import tensorflow as tf
import numpy as np
import math

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

from elephantcallscounter.data_processing.metadata_processing import MetadataProcessing
from elephantcallscounter.utils.path_utils import get_project_root


def find_number_of_clusters(dir_name):
    for img_name in os.listdir(dir_name):
        img = cv2.imread(os.path.join(dir_name, img_name), 0)
        # ret, threshold_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU, img)
        threshold_img = img
        threshold_img = threshold_img[60:410, 85:460]

        contours, _ = cv2.findContours(threshold_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        for c in contours:
            area = cv2.contourArea(c)
            if area > 500:
                continue
            rect = cv2.boundingRect(c)
            #if rect[2] < 7 or rect[3] < 7:
            #    continue
            x, y, w, h = rect
            x, y = x + 60, y + 60
            bb_width, bb_height = w + 60, h + 60
            cv2.rectangle()
            cv2.rectangle(
                img,
                (x - bb_width/2, y - bb_height/2),
                (x + bb_width/2, y + bb_height/2),
                (0, 255, 0),
                2
            )
            cv2.putText(img, 'Elephant Detected', (x + w + 10, y + h), 0, 0.3, (0, 255, 0))
            count += 1

        cv2.imshow("Show", img)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()


def draw(img, rects,color):
    for r in rects:
        p1 = (r[0], r[1])
        p2 = (r[0]+r[2], r[1]+r[3])
        cv2.rectangle(img, p1,p2, color,4)

    return img


def find_distance(pt1, pt2):
    return math.sqrt((pt2[1]-pt1[1])**2 + (pt2[0]-pt1[0])**2)


def filter_rectangles(rects):
    filtered_rects = [rects[0]]
    for rect in rects:
        for filtered_rect in filtered_rects:
            if find_distance(rect, filtered_rect) > 10:
                filtered_rects.append(rect)

    return filtered_rects


def find_matches(dir_name):
    # load image into variable
    template = cv2.imread(os.path.join(get_project_root(), 'data/elephant.png'), 0)

    for img_name in os.listdir(dir_name):
        # load template
        img = cv2.imread(os.path.join(dir_name, img_name), 0)

        # read height and width of template image
        w, h = template.shape[0], template.shape[1]

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.5
        loc = np.where(res > threshold)
        sorted_pts = sorted(zip(*loc), key = lambda t: res[t[0], t[1]], reverse = True)
        rects = []
        start_points_x = set()
        start_points_y = set()
        for pt in sorted_pts:
            if pt[0] not in start_points_x and pt[1] not in start_points_y:
                rects.append([pt[0], pt[1], w, h])
                start_points_x.add(pt[0])
                start_points_y.add(pt[1])

        rects = filter_rectangles(rects)
        img = draw(img, rects, (0, 0, 255))
        # img_rgb = cv2.resize(img, (800, 600))
        cv2.imshow("result", img)
        cv2.waitKey(10000)


def prepare_spectrograms():
    # dir_name = os.path.join(get_project_root(), 'data/spectrogram_images/CroppedTrainingSet/nn03d')
    dest_directory = os.path.join(get_project_root(), 'data/spectrogram_images/training_data')
    os.mkdir(dest_directory)
    labels = []
    # for file in os.listdir(dir_name):


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


# find_matches(os.path.join(get_project_root(), 'data/spectrogram_images/spectrograms'))
find_number_of_clusters(os.path.join(get_project_root(), 'data/spectrogram_images/spectrograms'))
build_model()
