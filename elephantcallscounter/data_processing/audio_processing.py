import logging

import librosa
import pydub

logger = logging.getLogger(__name__)


class AudioProcessing:
    @classmethod
    def crop_file(cls, start_sec, end_sec, file_name, destination_file):
        """This function crops the file from start time to the end time and writes to the
        destination file.

        :param start_sec:
        :type start_sec: float
        :param end_sec:
        :type end_sec: float
        :param file_name:
        :type file_name: string
        :param destination_file:
        :type destination_file: string
        :return int:
        """
        try:
            song = pydub.AudioSegment.from_wav(file_name)
            extract = song[start_sec:end_sec]
            extract.export(destination_file)
            return 1
        except pydub.exceptions.CouldntEncodeError:
            logger.info("Error cropping file: %s", destination_file)
            return -1

    @classmethod
    def load_data(cls, file_name, sr):
        """This function loads the audio data from the file.

        :param string file_name:
        :param int sr:
        :return: tuple
        """
        # Keeping audio at original sample rate
        signal, sr = librosa.load(file_name, sr=sr)
        logger.info("Duration of samples {}s".format(len(signal) / sr))
        return signal, sr
