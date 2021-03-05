import cv2

from elephantcallscounter.utils.path_utils import create_necessary_directories
from elephantcallscounter.utils.path_utils import join_paths


class Monochrome:
    def __init__(self, target_folder=''):
        self.target_folder = target_folder

    def create_monochrome(self, image_filename, write_file=False):
        print(f'Making monochrome image of file {image_filename}...')
        original_image = cv2.imread(image_filename)

        # grayscale
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        # monochrome
        (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

        if write_file:
            create_necessary_directories(self.target_folder)
            image_filename = image_filename.split('/')[-1]
            mono_path = join_paths([
                self.target_folder, image_filename.replace('spec_image_', 'mono_')
            ])
            cv2.imwrite(mono_path, blackAndWhiteImage)
            print(f'Monochrome image stored as {mono_path}')

        return blackAndWhiteImage
