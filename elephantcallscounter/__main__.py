#!/usr/bin/env python
import os

from data_analysis.analyse_sound_data import AnalyseSoundData

if __name__ == "__main__":
    analyse_sound_data = AnalyseSoundData(
        file_read_location = os.path.join(os.getcwd(), 'data/metadata/nn01a_20180126_000000_cropped.wav'),
        save_image_location = os.path.join(os.getcwd(), 'data/spectrogram_images/')
    )
    analyse_sound_data.analyse_audio()
