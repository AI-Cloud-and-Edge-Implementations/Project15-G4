import librosa
from librosa import display
import numpy as np
from matplotlib import pyplot as plt
import scipy

plt.rcParams['agg.path.chunksize'] = 10000


class Plots:
    def __init__(self, n_fft=2048, hop_length=128):
        self.n_fft = n_fft
        self.hop_length = hop_length

    def fft_plot(self, audio, sampling_rate, filename, plot=False):
        """ Fast fourier transform is for discrete signals while fourier transform is for continuous
        signals.

        :param plot:
        :param audio:
        :param sampling_rate:
        :return:
        """
        logger.info(f'Plotting FFT...')
        n = len(audio)
        T = 1 / sampling_rate
        yf = scipy.fft.fft(audio)

        xf = np.linspace(0.0, 1.0 / (2.0 * T), int(n / 2))

        fig, ax = plt.subplots()

        ax.plot(xf[::100], (2.0 / n * np.abs(yf[:n // 2]))[::100])
        plt.grid()
        plt.xlabel('Frequency -->')
        plt.ylabel('Magnitude')
        plt.xlim([0, 100])

        if plot:
            plt.savefig(f'data/spectrograms/fft_{filename}.png')
            # plt.show()

        logger.info('Done!')

    def plot_amp_time(self, samples, sampling_rate, plot=False):
        """ This tells us the loudness of the recording.

        :param plot:
        :param samples:
        :param sampling_rate:
        :return:
        """
        logger.info(f'Plotting loudness...')
        librosa.display.waveplot(y=samples, sr=sampling_rate)

        if plot:
            plt.xlabel('Time (ms)')
            plt.ylabel('Amplitude')
            plt.show()

        logger.info('Done!')

    def plot_and_save_spectrogram(self, input_data, sr, file_location, plot=False):
        """ Plot the spectrogram for the input data.

        :param input_data:
        :type input_data: librosa.Audio
        :param sr: 
        :type sr: int
        :param file_location:
        :type file_location: string
        :param plot: defaults to False
        :type plot: bool, optional
        """
        logger.info(f'Plotting and saving spectrogram for {file_location}...')

        stft_value = librosa.core.stft(input_data, n_fft=self.n_fft, hop_length=self.hop_length)
        spectrogram = np.abs(stft_value)

        fig, ax = plt.subplots()
        img = librosa.display.specshow(
            spectrogram, cmap='gray_r', ax=ax, sr=sr, hop_length=self.hop_length, x_axis='s', y_axis='linear'
        )
        plt.title('Spectrogram')
        plt.ylim([10, 50])
        plt.xlabel('time')
        plt.ylabel('frequency')

        # To add a legend: fig.colorbar(img, format='%+2.0f dB')

        fig.savefig(file_location)

        if plot:
            plt.show()

        logger.info('Done!')

    def plot_mel(self, input_data, sr, plot=False):
        """ Plots the mel spectrogram of the source data.

        :param input_data: 
        :type input_data: librosa.Audio
        :param sr: 
        :type sr: int
        :param plot: defaults to False
        :type plot: bool, optional
        """
        logger.info(f'Plotting the mel spectrogram...')
        n_mels = 128
        S = librosa.feature.melspectrogram(
            input_data, sr=sr, n_fft=self.n_fft, hop_length=self.hop_length, n_mels=n_mels, htk=True
        )
        S_DB = librosa.power_to_db(S, ref=np.max)

        librosa.display.specshow(S_DB, sr=sr, hop_length=self.hop_length, x_axis='time',
                                 y_axis='mel')
        plt.title('Mel Spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.ylim([0, 100])

        if plot:
            plt.show()

        logger.info('Done!')
