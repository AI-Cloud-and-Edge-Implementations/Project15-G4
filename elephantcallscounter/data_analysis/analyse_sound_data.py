import librosa
import librosa.display
import numpy as np
import os
import scipy

from data_processing.audio_processing import AudioProcessing
from data_transformations.filters import Filters
from data_visualizations.plots import Plots
from data_transformations.noise_reduction import NoiseReduction

class AnalyseSoundData:
    def __init__(self, file_read_location, save_image_location, sr, hop_length = 512):
        self.file_read_location = file_read_location
        self.save_image_location = save_image_location
        self.noise_reduce = NoiseReduction(hop_length, save_image_location)
        self.plot = Plots()
        self.hop_length = hop_length
        self.sr = sr

    def analyse_audio(self):
        # file_name = os.path.join(os.getcwd(), 'researchanddevelopment/segments/train/data/nn01a_20180126_000000.wav_segment_2_nan.wav')
        # .wav is lossless
        """
        crop_file(
            48860*1000, 
            48890*1000, 
            file_name = 'researchanddevelopment/metadata/nn01a_20180126_000000.wav',
            destination_file = 'researchanddevelopment/metadata/nn01a_20180126_000000_cropped.wav'
            )
        """
        input_signal, sr = AudioProcessing.load_data(self.file_read_location, self.sr)
        self.plot.plot_amp_time(input_signal, sr)
        duration = int(len(input_signal)/sr)
        # plots upto sampling rate/2(Nyquist theorem)
        # Filter requirements.
        fs = sr  # sample rate, Hz
        cutoff = 100  # desired cutoff frequency of the filter, Hz
        nyq = 0.5 * fs  # Nyquist Frequency
        order = 4  # sin wave can be approx represented as quadratic
        time = np.linspace(0, duration, len(input_signal), endpoint = False)
        lowpass_signal = Filters.butter_lowpass_filter(input_signal, cutoff, nyq, order, time)
        cutoff_high = 10
        highpass_signal = Filters.butter_highpass_filter(lowpass_signal, cutoff_high, nyq, order, time)
        self.plot.plot_and_save_spectrogram(
            highpass_signal, 
            sr, 
            file_location = os.path.join(self.save_image_location, 'spec_image.png')
        )
        self.plot.plot_mel(highpass_signal, sr)
        self.plot.fft_plot(highpass_signal, sr, plot = True)
        reduction_1 = self.noise_reduce.noise_reduce_and_plot_spectral_grating(highpass_signal, sr, duration)
        reduction_2 = self.noise_reduce.noise_reduce_and_plot_spectral_grating(reduction_1, sr, duration)
