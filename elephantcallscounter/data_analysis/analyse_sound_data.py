import numpy as np
import os
from pathlib import Path

from elephantcallscounter.data_processing.audio_processing import AudioProcessing
from elephantcallscounter.data_transformations.filters import Filters
from elephantcallscounter.data_visualizations.plots import Plots
from elephantcallscounter.data_transformations.noise_reduction import NoiseReduction


class AnalyseSoundData:
    def __init__(self, file_read_location, save_image_location, sr, hop_length=512):
        self.file_read_location = file_read_location
        self.save_image_location = save_image_location
        self.noise_reduce = NoiseReduction(hop_length, save_image_location)
        self.plot = Plots()
        self.hop_length = hop_length
        self.sr = sr

    def create_necessary_directories(self):
        """ This method creates the necessary directory structure.

        :return void:
        """
        Path(self.save_image_location).mkdir(parents=True, exist_ok=True)

    def analyse_audio(self):
        # .wav is lossless
        self.create_necessary_directories()

        input_signal, sr = AudioProcessing.load_data(self.file_read_location, self.sr)
        self.plot.plot_amp_time(input_signal, sr)

        duration = int(len(input_signal) / sr)
        # plots upto sampling rate/2(Nyquist theorem)
        # Filter requirements.
        fs = sr  # sample rate, Hz
        cutoff = 100  # desired cutoff frequency of the filter, Hz
        nyq = 0.5 * fs  # Nyquist Frequency
        order = 4  # sin wave can be approx represented as quadratic
        time = np.linspace(0, duration, len(input_signal), endpoint=False)

        lowpass_signal = Filters.butter_lowpass_filter(input_signal, cutoff, nyq, order, time)

        filename = self.file_read_location.split('/')[-1]

        cutoff_high = 10
        highpass_signal = Filters.butter_highpass_filter(lowpass_signal, cutoff_high, nyq, order, time)
        self.plot.plot_and_save_spectrogram(
            highpass_signal,
            sr,
            file_location=os.path.join(self.save_image_location, f'spec_image_{filename}.png')
        )
        self.plot.plot_mel(highpass_signal, sr)
        self.plot.fft_plot(highpass_signal, sr, plot=False)
        reduction_1 = self.noise_reduce.noise_reduce_and_plot_spectral_grating(highpass_signal, sr, duration)
        reduction_2 = self.noise_reduce.noise_reduce_and_plot_spectral_grating(reduction_1, sr, duration)
