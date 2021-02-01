import librosa
from pydub import AudioSegment

class AudioProcessing:
    @classmethod
    def crop_file(cls, start_sec, end_sec, file_name, destination_file):
        """ This function crops the file from start time to the end time and writes to the destination file.

        :param start_sec: 
        :type start_sec: float
        :param end_sec: 
        :type end_sec: float
        :param file_name: 
        :type file_name: string
        :param destination_file: 
        :type destination_file: string
        """
        song = AudioSegment.from_wav(file_name)
        extract = song[start_sec:end_sec]
        extract.export(destination_file)
    
    @classmethod
    def load_data(cls, file_name):
        """ This function loads the audio data from the file.

        :param file_name:
        :type file_name: string
        :return: signal, sr
        :rtype: tuple
        """
        # Keeping audio at original sample rate
        signal, sr = librosa.load(file_name, sr=1000)
        print('Duration of samples {}s'.format(len(signal)/sr))
        return signal, sr
 