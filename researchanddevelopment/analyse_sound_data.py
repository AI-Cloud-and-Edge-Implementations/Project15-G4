import librosa
import librosa.display
import numpy as np
import os
from matplotlib import pyplot as plt
from pydub import AudioSegment

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
    signal, sr = librosa.load('segments/train/data/nn01a_20180126_000000.wav_segment_2_nan.wav', sr=22050)
    return signal, sr


if __name__ == "__main__":
    # crop_file(0, 10000)
    # spectrogram_data()
    signal, sr = load_data()
    noise_len = 2  # seconds
    noise = band_limited_noise(min_freq=4000, max_freq=12000, samples=len(signal), samplerate=sr) * 10
    noise_clip = noise[:sr * noise_len]

    reduced_noise = nr.reduce_noise(signal, noise_clip=noise_clip, verbose=True)
