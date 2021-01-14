import os
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

for filename in os.listdir('../data-import/segments'):
    if filename.endswith('.wav'):
        try:
            print(f'Processing {filename}...')

            sample_rate, samples = wavfile.read('../data-import/segments/' + filename)  # check: mono files?
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
        except Exception as e:
            print('Error while creating spectrogram: ' + str(e))
