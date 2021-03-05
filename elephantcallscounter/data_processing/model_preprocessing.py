import splitfolders


class ModelPreprocessing:
    def __init__(self, input_folder, output_folder):
        self._input_folder = input_folder
        self._output_folder = output_folder

    def split_images_into_right_format(self, ratio=(.8, .1, .1)):
        splitfolders.ratio(
            self._input_folder,
            output=self._output_folder,
            seed=1337,
            ratio=ratio,
            group_prefix=None
        )
