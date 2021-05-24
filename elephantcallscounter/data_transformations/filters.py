import scipy
from matplotlib import pyplot as plt
from scipy.signal import butter


class Filters:
    @classmethod
    def butter_lowpass_filter(cls, data, cutoff, nyq, order, time, plot=False):
        """Lowpass filter for the input signal.

        :param data:
        :type data: librosa.Audio
        :param cutoff:
        :type cutoff: int
        :param nyq:
        :type nyq: float
        :param order:
        :type order: int
        :param time:
        :type time: ndarray
        :param plot: defaults to False
        :type plot: bool, optional
        :return:
        :rtype: librosa.Audio
        """
        normalized_cutoff = cutoff / nyq
        numerator_coeffs, denominator_coeffs = scipy.signal.butter(
            order, normalized_cutoff, btype="low", analog=False
        )
        filtered_signal = scipy.signal.lfilter(
            numerator_coeffs, denominator_coeffs, data
        )
        if plot:
            plt.plot(time, data, "b-", label="signal")
            plt.plot(time, filtered_signal, "g-", linewidth=2, label="filtered signal")
            plt.legend()
            plt.show()
        return filtered_signal

    @classmethod
    def butter_highpass_filter(cls, data, cutoff, nyq, order, time, plot=False):
        """High pass filter for the input signal.

        :param data:
        :type data: librosa.Audio
        :param cutoff:
        :type cutoff: int
        :param nyq:
        :type nyq: float
        :param order:
        :type order: int
        :param time:
        :type time: ndarray
        :param plot: defaults to False
        :type plot: bool, optional
        :return:
        :rtype: librosa.Audio
        """
        normalized_cutoff = cutoff / nyq
        numerator_coeffs, denominator_coeffs = scipy.signal.butter(
            order, normalized_cutoff, btype="high", analog=False
        )
        filtered_signal = scipy.signal.filtfilt(
            numerator_coeffs, denominator_coeffs, data
        )
        if plot:
            plt.plot(time, data, "b-", label="signal")
            plt.plot(time, filtered_signal, "g-", linewidth=2, label="filtered signal")
            plt.legend()
            plt.show()
        return filtered_signal
