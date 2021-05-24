import cv2
import math
import os
import pandas as pd
import logging

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths

logger = logging.getLogger(__name__)


class Boxing:
    def __init__(
            self, image_folder, target_folder, csv_file_path, monochrome, write_file=False
    ):
        self.image_folder = image_folder
        self.target_folder = target_folder
        self.csv_file_path = csv_file_path
        self.monochrome = monochrome
        self.write_file = write_file

    def write_box_to_file(self, image, elephants, image_filename):
        image_filename = image_filename.replace("mono_", "boxed_")
        os.makedirs(
            join_paths([self.target_folder, str(len(elephants))]), exist_ok=True
        )
        boxed_path = join_paths(
            [self.target_folder, str(len(elephants)), image_filename]
        )
        cv2.imwrite(boxed_path, image)
        logger.info(f"Boxed image stored as {boxed_path}")

    def create_boxes(self, image_filename):
        logger.info(f"Creating boxes for {self.image_folder + image_filename}...")

        image = self.monochrome.create_monochrome(
            join_paths([get_project_root(), self.image_folder, image_filename])
        )

        # cut off the axes
        # source images are 640 x 480 pixels
        y_top = 60
        y_bottom = 425
        x_left = 82
        x_right = 570
        ROI = image[y_top:y_bottom, x_left:x_right]

        thresh_inverse = cv2.bitwise_not(ROI)

        # create contours
        contours, hierarchy = cv2.findContours(
            thresh_inverse, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(ROI, contours, -1, (0, 255, 0), 1)

        # approximate contours to polygons + get bounding rects
        boxes = [None] * len(contours)

        elephant_rumbles = []

        for i, c in enumerate(contours):
            polygon = cv2.approxPolyDP(c, 3, True)
            boxes[i] = cv2.boundingRect(polygon)
            # (x, y, w, h), where x, y is the top left corner,
            # and w, h are the width and height respectively

            rect = boxes[i]
            width = rect[2]
            height = rect[3]

            # check if this can be an elephant
            if height > 5 and width > 50:
                middle_x = math.floor(rect[0] + (width / 2))
                middle_y = math.floor(rect[1] + (height / 2))

                cv2.rectangle(
                    ROI,
                    (int(boxes[i][0]), int(boxes[i][1])),
                    (int(boxes[i][0] + boxes[i][2]), int(boxes[i][1] + boxes[i][3])),
                    cv2.COLOR_BGR2HSV,
                    2,
                )

                elephant_rumbles.append((middle_x, middle_y))

        # count the elephants
        elephants = []
        for rumble in elephant_rumbles:
            # if the rumble has a similar frequency as others, don't count it
            # if the rumble has a similar mean time as others, don't count it
            similar_rumbles = list(
                filter(
                    lambda elephant: (
                            (abs(elephant[0] - rumble[0]) < 20)
                            or (abs(elephant[1] - rumble[1]) < 200)
                    ),
                    elephants,
                )
            )

            if len(similar_rumbles) < 1:
                logger.info(f"Unique elephant at {rumble}")
                elephants.append(rumble)
                cv2.drawMarker(
                    ROI, rumble, cv2.COLOR_LAB2LBGR, markerType=cv2.MARKER_STAR
                )

        logger.info(f"Found {len(elephants)} elephant(s) in image!")

        # put the ROI on top of the original image
        h, w = ROI.shape[0], ROI.shape[1]
        image[y_top: y_top + h, x_left: x_left + w] = ROI

        if self.write_file:
            self.write_box_to_file(image, elephants, image_filename)

        return image, len(elephants)

    def write_labels_to_csv_file(self, dataset):
        df = pd.DataFrame(dataset.items(), columns=["file_name", "number_of_elephants"])
        df.to_csv(self.csv_file_path)
