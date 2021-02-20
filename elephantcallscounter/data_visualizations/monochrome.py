import cv2


class Monochrome:
    def __init__(self, image_folder, target_folder):
        self.image_folder = image_folder
        self.target_folder = target_folder

    def create_monochrome(self, image_filename):
        print(f'Making monochrome image of file {image_filename}...')
        original_image = cv2.imread(self.image_folder + image_filename)

        # grayscale
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        # monochrome
        (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

        mono_path = self.target_folder + image_filename.replace('spec_image_', 'mono_')
        cv2.imwrite(mono_path, blackAndWhiteImage)
        print(f'Monochrome image stored as {mono_path}')

#
# monochrome('../data/spectrograms/train/',
#            'spec_image_nn01a_20180126_000000.wav_segment_6_nan.wav.png',
#            '../data/spectrograms/mono/')
