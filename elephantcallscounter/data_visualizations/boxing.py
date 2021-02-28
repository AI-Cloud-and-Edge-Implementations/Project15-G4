import cv2
import math


class Boxing:
    def __init__(self, image_folder, target_folder):
        self.image_folder = image_folder
        self.target_folder = target_folder

    @staticmethod
    def same_elephant(rumble1, rumble2):
        """
        Compare two rumbles and determine whether they belong to the same elephant.
        Each rumble is in the (x,y) format where x is the middle time of the box, y is the middle frequency.
        We compare the distances in square roots; more distance is more likely to be a different elephant.
        :return: True if the rumbles belong the same elephant, False if not
        """
        print(f'comparing rumbles {rumble1} and {rumble2}...')
        # compare the time
        if ((rumble1[0] - rumble2[0]) ** 2) < 20000:
            # print('time overlaps')
            return True

        # compare the frequency
        if ((rumble1[1] - rumble2[1]) ** 2) < 3000:
            # print('frequency overlaps')
            return True

        # print('different')
        return False

    def create_contours_and_boxes(self, image_filename):
        """
        Create rectangles for elephant rumbles
        :param image_filename:
        :return:
        """
        print(f'Creating boxes for {self.image_folder + image_filename}...')

        image = cv2.imread(self.image_folder + image_filename)

        # cut off the axes
        # source images are 640 x 480 pixels
        y_top = 60
        y_bottom = 425
        x_left = 82
        x_right = 570
        ROI = image[y_top:y_bottom, x_left:x_right]

        gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        thresh_inverse = cv2.bitwise_not(gray)

        # create contours
        contours, hierarchy = cv2.findContours(thresh_inverse, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(ROI, contours, -1, (0, 255, 0), 1)

        # approximate contours to polygons + get bounding rects
        boxes = [None] * len(contours)

        elephant_rumbles = []

        for i, c in enumerate(contours):
            polygon = cv2.approxPolyDP(c, 3, True)
            boxes[i] = cv2.boundingRect(polygon)
            # (x, y, w, h), where x, y is the top left corner, and w, h are the width and height respectively

            rect = boxes[i]
            width = rect[2]
            height = rect[3]

            # check if this can be an elephant
            if height > 5 and width > 70:
                middle_x = math.floor(rect[0] + (width / 2))
                middle_y = math.floor(rect[1] + (height / 2))

                cv2.rectangle(ROI, (int(boxes[i][0]), int(boxes[i][1])),
                              (int(boxes[i][0]+boxes[i][2]), int(boxes[i][1]+boxes[i][3])), cv2.COLOR_BGR2HSV, 2)

                elephant_rumbles.append((middle_x, middle_y))

        # count the elephants
        elephants = []
        for rumble in elephant_rumbles:
            # if the rumble has a similar frequency as others, don't count it
            # if the rumble has a similar mean time as others, don't count it
            similar_rumbles = list(filter(lambda elephant: (self.same_elephant(rumble, elephant)), elephants))

            if len(similar_rumbles) < 1:
                print(f'Unique elephant at {rumble}')
                elephants.append(rumble)
                cv2.drawMarker(ROI, rumble, cv2.COLOR_LAB2LBGR, markerType=cv2.MARKER_STAR)

        print(f'Found {len(elephants)} elephant(s) in image!')

        # put the ROI on top of the original image
        h, w = ROI.shape[0], ROI.shape[1]
        image[y_top:y_top+h, x_left:x_left+w] = ROI

        boxed_path = self.target_folder + str(len(elephants)) + '_' + image_filename.replace('mono_', 'boxed_')
        cv2.imwrite(boxed_path, image)
        print(f'Boxed image stored as {boxed_path}')


# b = Boxing('../data/spectrograms/mono/', '../data/spectrograms/boxed2/')
# b.create_contours_and_boxes('mono_nn01d_20180730_000000.wav_segment_366_nan.wav.png')

# b.create_contours_and_boxes('mono_nn10a_20180702_000000.wav_segment_3057_nan.wav.png')
