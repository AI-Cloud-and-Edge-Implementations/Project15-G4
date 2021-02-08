#!/usr/bin/env python
import os

from elephantcallscounter.data_analysis.analyse_sound_data import AnalyseSoundData
from elephantcallscounter.data_processing.segment_files import ready_file_segments

if __name__ == "__main__":
    ready_file_segments()
    analyse_sound_data = AnalyseSoundData(
        file_read_location = os.path.join(os.getcwd(), 'data/metadata/nn01a_20180126_000000_cropped.wav'),
        save_image_location = os.path.join(os.getcwd(), 'data/spectrogram_images/'),
        sr = 1000,
        hop_length = 256
    )
    analyse_sound_data.analyse_audio()
