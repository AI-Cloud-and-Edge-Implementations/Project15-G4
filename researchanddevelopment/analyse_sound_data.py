import librosa
import librosa.display
import numpy as np
import os
import scipy
import noisereduce as nr

from audio_processing import AudioProcessing
from filters import Filters
from plots import Plots

hop_length = 512


def noise_reduce_and_plot(signal, sr, duration, plot = False):
    """ Reduce the noisy file and plot the spectrogram.

    :param signal: 
    :type signal: librosa.Audio
    :param sr: 
    :type sr: int
    :param duration: 
    :type duration: int
    :param plot: defaults to False
    :type plot: bool, optional
    :return: 
    :rtype: librosa.Audio
    """
    noise_clip = signal[0:duration*1000]
    reduced_noise = nr.reduce_noise(
        signal, noise_clip=noise_clip, verbose=False, n_grad_freq=3, hop_length=512
    )
    Plots.plot_and_save_spectrogram(reduced_noise, sr, image_name='noise_reduced_spec.png')
    if plot:
        Plots.plot_mel(reduced_noise)
        Plots.fft_plot(reduced_noise, sr)
    return reduced_noise

def main():
    file_name = os.path.join(os.getcwd(), 'metadata/nn01a_20180126_000000_cropped.wav')
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
    input_signal, sr = AudioProcessing.load_data(file_name)
    Plots.plot_amp_time(input_signal, sr)
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
    Plots.plot_and_save_spectrogram(highpass_signal, sr, image_name = 'spec_image.png')
    Plots.plot_mel(highpass_signal, sr)
    Plots.fft_plot(highpass_signal, sr, plot = False)
    reduction_1 = noise_reduce_and_plot(highpass_signal, sr, duration)
    reduction_2 = noise_reduce_and_plot(reduction_1, sr, duration)


if __name__ == "__main__":
    main()
