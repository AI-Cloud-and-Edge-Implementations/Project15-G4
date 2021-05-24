import os
import logging
import noisereduce as nr
from elephantcallscounter.data_visualizations.plots import Plots

logger = logging.getLogger(__name__)


class NoiseReduction:
    def __init__(self, save_image_location, hop_length=512):
        """Constructor.

        :param int hop_length:
        :return void:
        """
        self._hop_length = hop_length
        self.save_image_location = save_image_location
        self.plot = Plots()

    def noise_reduce_and_plot_spectral_grating(
            self, signal, sr, duration, filename, plot=False
    ):
        """Reduce the noisy file and plot the spectrogram.

        :param filename:
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
        logger.info("Reducing noise...")

        noise_clip = signal[0: duration * 1000]
        reduced_noise = nr.reduce_noise(
            signal,
            noise_clip=noise_clip,
            verbose=False,
            n_grad_freq=3,
            hop_length=self._hop_length,
        )
        if plot:
            self.plot.plot_and_save_spectrogram(
                reduced_noise,
                sr,
                file_location=os.path.join(
                    self.save_image_location, "noise_reduced_spec.png"
                ),
            )
            self.plot.fft_plot(reduced_noise, sr, filename, plot)

        logger.info("Done!")
        return reduced_noise
