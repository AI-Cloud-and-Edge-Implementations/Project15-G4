from elephantcallscounter.services.data_analysis_service import analyse_sound_data
from elephantcallscounter.services.data_analysis_service import create_mono_spectrograms
from elephantcallscounter.services.data_analysis_service import find_elephants_in_images
from elephantcallscounter.management.commands.data_analysis_commands import run_cnn


def pipeline_run(file_path):
    analyse_sound_data(
        file_path = file_path,
        dest_path = 'data/spectrogram_demo'
    )
    create_mono_spectrograms(
        'data/spectrogram_demo',
        'data/spectrogram_demo_mono'
    )
    find_elephants_in_images(
        'data/spectrogram_demo_mono',
        'data/spectrogram_demo_bb',
        ''
    )
    run_cnn('data/spectrogram_demo_bb')
