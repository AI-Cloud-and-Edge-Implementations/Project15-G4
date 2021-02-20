import cv2
import numpy as np
import pandas as pd
import os

from elephantcallscounter.utils.math_utils import find_distance
from elephantcallscounter.utils.path_utils import get_project_root


def draw(img, rects, color):
    for r in rects:
        p1 = (r[0], r[1])
        p2 = (r[0] + r[2], r[1] + r[3])
        cv2.rectangle(img, p1, p2, color, 4)

    return img


def filter_rectangles(rects):
    filtered_rects = [rects[0]]
    for rect in rects:
        for filtered_rect in filtered_rects:
            if find_distance(rect, filtered_rect) > 200:
                filtered_rects.append(rect)

    return filtered_rects


def find_matches(img):
    # load image into variable
    template = cv2.imread(os.path.join(get_project_root(), 'data/elephant.png'), 0)

    # read height and width of template image
    w, h = template.shape[0], template.shape[1]

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res > threshold)
    sorted_pts = sorted(zip(*loc), key = lambda t: res[t[0], t[1]], reverse = True)

    if not sorted_pts:
        print('no rects')
        return []

    rects = [[sorted_pts[0][0], sorted_pts[0][1], w, h]]
    
    return rects


def threshold_image(img):
    ret, threshold_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    return threshold_img


def display_image(img, name):
    cv2.imshow(name, img)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()


def find_number_of_clusters(dir_name, dest_folder, display_message = False):
    count = 0
    file_elephants = {}
    threshold_y = 70
    threshold_x = 85
    threshold_h = 410
    threshold_w = 560

    for img_name in os.listdir(dir_name):
        dest_file = os.path.join(dest_folder, "bb_" + img_name)
        img = cv2.imread(os.path.join(dir_name, img_name), 0)
        threshold_img = img[threshold_y:threshold_h, threshold_x:threshold_w]
        contours, _ = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        filtered_rects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 20000:
                continue
            rect = cv2.boundingRect(contour)
            filtered_rects.append(rect)
        if dest_file == '/home/abhishekh/personalProjects/Microsoft-Project-15-Team-4/elephantcallscounter/data/spectrogram_bb/bb_mono_nn06a_20180912_000000.wav_segment_416_nan.wav.png':
            print('Waiting here')

        if len(filtered_rects) == 0:
            filtered_rects = find_matches(threshold_img)
            if not filtered_rects:
                print('No bounding boxes for img: {}'.format(img_name))
                continue

        file_elephants[img_name] = len(filtered_rects)

        for rect in filtered_rects:
            x, y, w, h = rect
            x, y = x + threshold_x, y + threshold_y
            left_x, left_y = x, y
            right_x, right_y = x + w, y + h
            cv2.rectangle(
                img,
                (left_x, left_y),
                (right_x, right_y),
                (0, 255, 0),
                2
            )
            if display_message:
                cv2.putText(
                    img, 'Elephant Detected',
                    (x + w + 10, int(y - h)), 0, 0.3, (0, 255, 0)
                )

        count += 1
        print('BB for image done: ', count)
        cv2.imwrite(dest_file, img)

    df = pd.DataFrame(file_elephants.items(), columns = ['file_name', 'number_of_elephants'])
    print(df)
