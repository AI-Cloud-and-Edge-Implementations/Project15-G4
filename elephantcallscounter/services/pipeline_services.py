from elephantcallscounter.services.data_analysis_service import analyse_sound_data
from elephantcallscounter.services.data_analysis_service import create_mono_spectrograms
from elephantcallscounter.services.data_analysis_service import find_elephants_in_images
from elephantcallscounter.management.commands.data_analysis_commands import run_cnn
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.file_utils import get_files_in_dir


def pipeline_run(file_path):
    analyse_sound_data(
        file_path = file_path,
        dest_path = join_paths([get_project_root(), 'data/demo/spectrogram'])
    )
    spectrogram_files_full = [
        join_paths([get_project_root(), 'data/demo/spectrogram', file])
        for file in get_files_in_dir('data/demo/spectrogram')
    ]
    create_mono_spectrograms(
        spectrogram_files_full,
        target_folder = join_paths([get_project_root(), 'data/demo/spectrogram_mono']),
        write_file = True
    )
    find_elephants_in_images(
        join_paths([get_project_root(), 'data/demo/spectrogram_mono']),
        join_paths([get_project_root(), 'data/demo/spectrogram_bb']),
        join_paths([get_project_root(), 'data/demo/test_spec_image_labels.csv'])
    )
    value = run_cnn('binaries/resnet', 'data/demo/spectrogram_bb')
    return value
