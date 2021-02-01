import librosa
import librosa.display
import numpy as np
import os
from matplotlib import pyplot as plt
from pydub import AudioSegment
import scipy
from scipy.signal import butter, filtfilt
from noisereduce.utils import int16_to_float32


import noisereduce as nr

n_fft = 4096
hop_length = 128


def crop_file(start_sec, end_sec, file_name, destination_file):
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


def load_data(file_name):
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


def fft_plot(audio, sampling_rate, plot = False):
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


def plot_amp_time(samples, sampling_rate, plot = False):
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


def butter_lowpass_filter(data, cutoff, nyq, order, time, plot = False):
    """ Lowpass filter for the input signal.

    :param data: [description]
    :type data: [type]
    :param cutoff: [description]
    :type cutoff: [type]
    :param nyq: [description]
    :type nyq: [type]
    :param order: [description]
    :type order: [type]
    :param time: [description]
    :type time: [type]
    :param plot: [description], defaults to False
    :type plot: bool, optional
    :return: [description]
    :rtype: [type]
    """
    normalized_cutoff = cutoff / nyq
    numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff, btype='low', analog=False)
    filtered_signal = scipy.signal.lfilter(numerator_coeffs, denominator_coeffs, data)
    if plot:
        plt.plot(time, data, 'b-', label = 'signal')
        plt.plot(time, filtered_signal, 'g-', linewidth = 2, label = 'filtered signal')
        plt.legend()
        plt.show()
    return filtered_signal


def butter_highpass_filter(data, cutoff, nyq, order, time, plot = False):
    """ High pass filter for the input signal.

    :param data: [description]
    :type data: [type]
    :param cutoff: [description]
    :type cutoff: [type]
    :param nyq: [description]
    :type nyq: [type]
    :param order: [description]
    :type order: [type]
    :param time: [description]
    :type time: [type]
    :param plot: [description], defaults to False
    :type plot: bool, optional
    :return: [description]
    :rtype: [type]
    """
    normalized_cutoff = cutoff / nyq
    numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff, btype='high', analog=False)
    filtered_signal = scipy.signal.filtfilt(numerator_coeffs, denominator_coeffs, data)
    if plot:
        plt.plot(time, data, 'b-', label = 'signal')
        plt.plot(time, filtered_signal, 'g-', linewidth = 2, label = 'filtered signal')
        plt.legend()
        plt.show()
    return filtered_signal


def plot_spectrogram(input_data, sr, image_name, plot = False):
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
    fig.savefig(os.path.join(os.getcwd(), 'researchanddevelopment/spectrogram_images/', image_name))
    if plot:
        plt.show()


def plot_mel(input_data, sr, plot = False):
    """ Plots the mel spectrogram of the source data.

    :param input_data: 
    :type input_data: librosa.Audio
    :param sr: 
    :type sr: int
    :param plot: [description], defaults to False
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

def noise_reduce_and_plot(signal, sr, duration, plot = False):
    """ Reduce the noisy file and plot the spectrogram.

    :param signal: [description]
    :type signal: [type]
    :param sr: [description]
    :type sr: [type]
    :param duration: [description]
    :type duration: [type]
    :param plot: [description], defaults to False
    :type plot: bool, optional
    :return: [description]
    :rtype: [type]
    """
    noise_clip = signal[0:duration*1000]
    reduced_noise = nr.reduce_noise(
        signal, noise_clip=noise_clip, verbose=False, n_grad_freq=3, hop_length=512
    )
    plot_spectrogram(reduced_noise, sr, image_name='noise_reduced_spec.png')
    if plot:
        plot_mel(reduced_noise)
        fft_plot(reduced_noise, sr)
    return reduced_noise

def main():
    file_name = os.path.join(os.getcwd(), 'researchanddevelopment/metadata/nn01a_20180126_000000_cropped.wav')
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
    input_signal, sr = load_data(file_name)
    plot_amp_time(input_signal, sr)
    duration = int(len(input_signal)/sr)
    # plots upto sampling rate/2(Nyquist theorem)
    # Filter requirements.
    fs = sr  # sample rate, Hz
    cutoff = 100  # desired cutoff frequency of the filter, Hz
    nyq = 0.5 * fs  # Nyquist Frequency
    order = 4  # sin wave can be approx represented as quadratic
    time = np.linspace(0, duration, len(input_signal), endpoint = False)
    lowpass_signal = butter_lowpass_filter(input_signal, cutoff, nyq, order, time)
    cutoff_high = 10
    highpass_signal = butter_highpass_filter(lowpass_signal, cutoff_high, nyq, order, time)
    plot_spectrogram(highpass_signal, sr, image_name = 'spec_image.png')
    plot_mel(highpass_signal, sr)
    fft_plot(highpass_signal, sr, plot = False)
    reduction_1 = noise_reduce_and_plot(highpass_signal, sr, duration)
    reduction_2 = noise_reduce_and_plot(reduction_1, sr, duration)


if __name__ == "__main__":
    main()
