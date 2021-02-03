import os

from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt


def create_spectrograms():
    for filename in os.listdir('../data-import/segments'):
        if filename.endswith('.wav'):
            try:
                print(f'Processing {filename}...')
                scipy_plot(filename)
            except Exception as e:
                print('Error while creating spectrogram: ' + str(e))


def scipy_plot(filename):
    sample_rate, samples = wavfile.read('../data-import/segments/' + filename)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, mode='magnitude')

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)

    # not sure if we need this, might add confusion in deep learning
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')

    plt.colorbar()

    # plt.show()  # for in notebooks

    spectrogram_path = 'spectrograms/' + filename.rsplit('.', 1)[0] + '.png'
    print(f'Exporting spectrogram to {spectrogram_path}...')
    plt.savefig(spectrogram_path)
