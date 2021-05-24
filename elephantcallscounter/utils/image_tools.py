import cv2
import numpy as np


def draw(img, rects, color):
    """Add a rectangle to an image.

    :param np.ndarray img:
    :param cv2.Rectangle rects:
    :param cv2.Color color:
    :return np.ndarray:
    """
    for r in rects:
        p1 = (r[0], r[1])
        p2 = (r[0] + r[2], r[1] + r[3])
        cv2.rectangle(img, p1, p2, color, 4)

    return img


def find_matches(img, template):
    """Match an image to a template and return the matched points sorted.

    :param np.ndarray img:
    :param np.ndarray template:
    :return list:
    """

    # read height and width of template image
    w, h = template.shape[0], template.shape[1]

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res > threshold)
    sorted_pts = sorted(zip(*loc), key=lambda t: res[t[0], t[1]], reverse=True)

    return sorted_pts


def threshold_image(img):
    """Threshold and input image using binary thresholding.

    :param np.ndarray img:
    :return np.ndarray:
    """
    ret, threshold_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    return threshold_img


def display_image(img, name):
    """This displays the image with the passed name in a new window.

    :param np.ndarray img:
    :param string name:
    :return void:
    """
    cv2.imshow(name, img)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()


def add_rectangles_to_img(
    new_rects, threshold_x, threshold_y, img, display_message=False
):
    """This adds bounding box rectangles to an image.

    :param list new_rects:
    :param float threshold_x:
    :param float threshold_y:
    :param np.ndarray img:
    :param bool display_message:
    :return void:
    """
    for rect in new_rects:
        x, y, w, h = rect
        x, y = x + threshold_x, y + threshold_y
        left_x, left_y = x, y
        right_x, right_y = x + w, y + h
        cv2.rectangle(img, (left_x, left_y), (right_x, right_y), (0, 255, 0), 2)
        if display_message:
            cv2.putText(
                img, "Elephant Detected", (x + w + 10, int(y - h)), 0, 0.3, (0, 255, 0)
            )


def get_contours_based_on_area(img, area_threshold=20000):
    """This method returns the contours based on an area threshold.

    :param np.ndarray img:
    :param int area_threshold:
    :return cv2.Rectangle:
    """
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_rects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > area_threshold:
            continue
        rect = cv2.boundingRect(contour)
        filtered_rects.append(rect)

    return filtered_rects
