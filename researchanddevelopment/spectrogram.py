import librosa
import librosa.display
import numpy as np
from matplotlib import pyplot as plt
from pydub import AudioSegment


def crop_file(start_sec, end_sec):
    filename = 'nn01a_20180126_000000.wav'
    song = AudioSegment.from_wav(filename)
    extract = song[start_sec:end_sec]
    extract.export('nn01a_20180126_000000_cropped.wav')


def spectrogram_data():
    n_fft = 2048
    hop_length = 512

    count = 0
    # dir_path = 'segments/train/data/'
    # for file in os.listdir(dir_path):
    # file_path = dir_path + file
    y, sr = librosa.load('nn01a_20180126_000000_cropped.wav', duration = 30)
    fig, ax = plt.subplots(nrows = 2, ncols = 1, sharex = True)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref = np.max)
    img = librosa.display.specshow(D, y_axis = 'linear', x_axis = 'time', sr = sr, ax = ax[0])
    ax[0].set(title = 'Linear-frequency power spectrogram')
    ax[0].label_outer()
    # plt.savefig('spectrum_file.png')
    # if count == 100:
    #    break
    # count += 1


if __name__ == "__main__":
    # crop_file(48860*1000, 48900*1000)
    spectrogram_data()
