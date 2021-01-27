import librosa
import librosa.display
import numpy as np
import os
from matplotlib import pyplot as plt
from pydub import AudioSegment
import scipy
from scipy.signal import butter, filtfilt


import noisereduce as nr


def crop_file(start_sec, end_sec):
    filename = 'metadata/nn01a_20180126_000000.wav'
    song = AudioSegment.from_wav(filename)
    extract = song[start_sec:end_sec]
    extract.export('metadata/nn01a_20180126_000000_cropped.wav')


def fftnoise(f):
    f = np.array(f, dtype="complex")
    Np = (len(f) - 1) // 2
    phases = np.random.rand(Np) * 2 * np.pi
    phases = np.cos(phases) + 1j * np.sin(phases)
    f[1 : Np + 1] *= phases
    f[-1 : -1 - Np : -1] = np.conj(f[1 : Np + 1])
    return np.fft.ifft(f).real

def band_limited_noise(min_freq, max_freq, samples=1024, samplerate=1):
    freqs = np.abs(np.fft.fftfreq(samples, 1 / samplerate))
    f = np.zeros(samples)
    f[np.logical_and(freqs >= min_freq, freqs <= max_freq)] = 1
    return fftnoise(f)


def spectrogram_data(signal, sr):
    n_fft = 2048
    hop_length = 512

    count = 0
    #dir_path = 'segments/train/data/'
    #for file in os.listdir(dir_path):
    # file_path = dir_path + file

    stft = librosa.core.stft(signal, hop_length=hop_length, n_fft=n_fft)

    spectrogram = np.abs(stft)
    log_spectrogram = librosa.amplitude_to_db(spectrogram)
    librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length)
    plt.xlabel('time')
    plt.ylabel('frequency')
    plt.colorbar()
    plt.show()
    #if count == 100:
    #    break
    # count += 1


def load_data():
    # signal, sr = librosa.load('metadata/nn01a_20180126_000000_cropped.wav', sr=22050)
    # Keeping audio at original sample rate
    signal, sr = librosa.load('metadata/nn01a_20180126_000000_cropped.wav', sr=None)
    print('Duration of samples {}s'.format(len(signal)/sr))
    return signal, sr


def fft_plot(audio, sampling_rate):
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
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    plt.grid()
    plt.xlabel('Frequency -->')
    plt.ylabel('Magnitude')
    return plt.show()


def plot_amp_time(samples, sampling_rate):
    """ This tells us the loudness of the recording.

    :param samples:
    :param sampling_rate:
    :return:
    """
    librosa.display.waveplot(y = samples, sr = sampling_rate)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.show()


def spectrogram(samples, sample_rate, stride_ms = 10.0,
                window_ms = 20.0, max_freq = None, eps = 1e-14):
    stride_size = int(0.001 * sample_rate * stride_ms)
    window_size = int(0.001 * sample_rate * window_ms)

    # Extract strided windows
    truncate_size = (len(samples) - window_size) % stride_size
    samples = samples[:len(samples) - truncate_size]
    nshape = (window_size, (len(samples) - window_size) // stride_size + 1)
    nstrides = (samples.strides[0], samples.strides[0] * stride_size)
    windows = np.lib.stride_tricks.as_strided(samples,
                                              shape = nshape, strides = nstrides)

    assert np.all(windows[:, 1] == samples[stride_size:(stride_size + window_size)])

    # Window weighting, squared Fast Fourier Transform (fft), scaling
    weighting = np.hanning(window_size)[:, None]

    fft = np.fft.rfft(windows * weighting, axis = 0)
    fft = np.absolute(fft)
    fft = fft ** 2

    scale = np.sum(weighting ** 2) * sample_rate
    fft[1:-1, :] *= (2.0 / scale)
    fft[(0, -1), :] /= scale

    # Prepare fft frequency list
    freqs = float(sample_rate) / window_size * np.arange(fft.shape[0])

    # Compute spectrogram feature
    ind = np.where(freqs <= max_freq)[0][-1] + 1
    specgram = np.log(fft[:ind, :] + eps)
    return specgram


def butter_lowpass_filter(data, cutoff, nyq, order, time):
    normalized_cutoff = cutoff / nyq
    numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff, btype='low', analog=False)
    filtered_signal = scipy.signal.lfilter(numerator_coeffs, denominator_coeffs, data)
    plt.plot(time, input_signal, 'b-', label = 'signal')
    plt.plot(time, filtered_signal, 'g-', linewidth = 2, label = 'filtered signal')
    plt.legend()
    plt.show()
    return filtered_signal


def butter_highpass_filter(data, cutoff, nyq, order, time):
    normalized_cutoff = cutoff / nyq
    numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff, btype='high', analog=False)
    filtered_signal = scipy.signal.filtfilt(numerator_coeffs, denominator_coeffs, data)
    plt.plot(time, input_signal, 'b-', label = 'signal')
    plt.plot(time, filtered_signal, 'g-', linewidth = 2, label = 'filtered signal')
    plt.legend()
    plt.show()
    return filtered_signal


def plot_spectrogram(input_data):
    n_fft = 2048
    hop_length = 512
    stft = librosa.core.stft(input_data, hop_length=hop_length, n_fft=n_fft)
    spectrogram = np.abs(stft)
    log_spectrogram = librosa.amplitude_to_db(spectrogram)
    librosa.display.specshow(
        log_spectrogram, sr=sr, hop_length=hop_length, x_axis = 's', y_axis = 'log')
    plt.xlabel('time')
    plt.ylabel('frequency')
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    # .wav is lossless
    # crop_file(48860*1000, 49000*1000)
    # spectrogram_data()
    input_signal, sr = load_data()
    plot_amp_time(input_signal, sr)
    duration = int(len(input_signal)/sr)
    # plots upto sampling rate/2(Nyquist theorem)
    # Filter requirements.
    fs = sr  # sample rate, Hz
    cutoff = 100  # desired cutoff frequency of the filter, Hz
    nyq = 0.5 * fs  # Nyquist Frequency
    order = 2  # sin wave can be approx represented as quadratic
    time = np.linspace(0, duration, len(input_signal), endpoint = False)
    lowpass_signal = butter_lowpass_filter(input_signal, cutoff, nyq, order, time)
    cutoff_high = 10
    highpass_signal = butter_highpass_filter(lowpass_signal, cutoff_high, nyq, order, time)
    fft_plot(highpass_signal, sr)
    noise_clip = highpass_signal[0:duration*1000]
    reduced_noise = nr.reduce_noise(highpass_signal, noise_clip=noise_clip, verbose=True)
    plot_spectrogram(reduced_noise)
