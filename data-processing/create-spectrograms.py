import os

import numba
from scipy import signal
from scipy.io import wavfile
# import librosa
import matplotlib.pyplot as plt
import numpy


def create_spectrograms():
    for filename in os.listdir('../data-import/segments'):
        if filename.endswith('.wav'):
            try:
                print(f'Processing {filename}...')
                scipi_plot(filename)
            except Exception as e:
                print('Error while creating spectrogram: ' + str(e))


# def librosa_plot():
#     segment = librosa.load(filename, sr=None)
#
#     # converting into energy levels(dB)
#     Xdb = librosa.amplitude_to_db(abs(librosa.stft(segment)))
#
#     plt.figure(figsize=(20, 5))
#     librosa.display.specshow(Xdb, x_axis='time', y_axis='hz')
#
#     # plt.colorbar()

def scipi_plot(filename):
    sample_rate, samples = wavfile.read('../data-import/segments/' + filename)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)

    # not sure if we need this, might add confusion in deep learning
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')

    # plt.show()  # for in notebooks
    spectrogram_path = 'spectrograms/' + filename.rsplit('.', 1)[0] + '.png'
    print(f'Exporting spectrogram to {spectrogram_path}...')
    plt.savefig(spectrogram_path)


# def plot_amplitude(samples, sample_rate):
#     sound = samples / (2. ** 15)
#
#     mySoundShape = sound.shape
#     samplePoints = float(sound.shape[0])
#
#     #Get duration of sound file
#     signalDuration = sound.shape[0] / sample_rate
#
#
#     #Plotting the tone
#
#     # We can represent sound by plotting the pressure values against time axis.
#     #Create an array of sample point in one dimension
#     timeArray = numpy.arange(0, samplePoints, 1)
#
#     timeArray = timeArray / sample_rate
#
#     #Scale to milliSeconds
#     timeArray = timeArray * 1000
#
#     #Plot the tone
#     plt.plot(timeArray, sound)   # , color='G')
#     plt.xlabel('Time (ms)')
#     plt.ylabel('Amplitude')

if __name__ == '__main__':
    create_spectrograms()
