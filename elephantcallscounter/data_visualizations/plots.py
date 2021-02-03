import librosa
import numpy as np
from matplotlib import pyplot as plt
import os
import scipy

n_fft = 4096
hop_length = 512


class Plots:
    @classmethod
    def fft_plot(cls, audio, sampling_rate, plot = False):
        """ Fast fourier transform is for discrete signals while fourier transform is for continuous
        signals.

        :param audio:
        :param sampling_rate:
        :return:
        """
        n = len(audio)
        T = 1/sampling_rate
        yf = scipy.fft.fft(audio)
        xf = np.linspace(0.0, 1.0/(2.0*T), n/2)
        if plot:
            fig, ax = plt.subplots()
            ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
            plt.grid()
            plt.xlabel('Frequency -->')
            plt.ylabel('Magnitude')
            plt.xlim([0,100])
            plt.show()

    @classmethod
    def plot_amp_time(cls, samples, sampling_rate, plot = False):
        """ This tells us the loudness of the recording.

        :param samples:
        :param sampling_rate:
        :return:
        """
        librosa.display.waveplot(y = samples, sr = sampling_rate)
        if plot:
            plt.xlabel('Time (seconds)')
            plt.ylabel('Amplitude')
            plt.show()

    @classmethod
    def plot_and_save_spectrogram(cls, input_data, sr, file_location, plot = False):
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
        stft_value = librosa.core.stft(input_data, n_fft=n_fft, hop_length=hop_length)
        spectrogram = np.abs(stft_value)
        log_spectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)
        fig, ax = plt.subplots()
        img = librosa.display.specshow(
            spectrogram, cmap='gray_r', ax = ax, sr=sr, hop_length=hop_length, x_axis = 's', y_axis = 'linear'
        )
        plt.title('Spectrogram')
        plt.ylim([0,100])
        plt.xlabel('time')
        plt.ylabel('frequency')
        fig.colorbar(img, format = '%+2.0f dB') 
        fig.savefig(file_location)
        if plot:
            plt.show()

    @classmethod
    def plot_mel(cls, input_data, sr, plot = False):
        """ Plots the mel spectrogram of the source data.

        :param input_data: 
        :type input_data: librosa.Audio
        :param sr: 
        :type sr: int
        :param plot: defaults to False
        :type plot: bool, optional
        """
        n_mels = 128
        S = librosa.feature.melspectrogram(input_data, sr = sr, n_fft = n_fft, hop_length = hop_length,
                                        n_mels = n_mels, htk = True)
        S_DB = librosa.power_to_db(S, ref = np.max)
        if plot:
            librosa.display.specshow(S_DB, sr = sr, hop_length = hop_length, x_axis = 'time',
                                y_axis = 'mel')
            plt.title('Mel Spectrogram')
            plt.colorbar(format = '%+2.0f dB')
            plt.ylim([0,100])
            plt.show()
