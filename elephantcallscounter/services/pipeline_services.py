import ast
import requests

from elephantcallscounter.services.data_analysis_service import analyse_sound_data
from elephantcallscounter.services.data_analysis_service import create_mono_spectrograms
from elephantcallscounter.services.data_analysis_service import find_elephants_in_images
from elephantcallscounter.management.commands.data_analysis_commands import run_cnn
from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths
from elephantcallscounter.utils.file_utils import get_files_in_dir


def pipeline_run(file_path, csv_file_path):
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
        join_paths([get_project_root(), csv_file_path])
    )
    value = run_cnn('binaries/resnet', 'data/demo/spectrogram_bb')
    url = 'http://0.0.0.0:5000/elephants/elephants_count/'
    r = requests.get(url = url, params = {
        'start_time': '2020-01-10 06:30:23',
        'end_time': '2021-01-11 06:30:23'
    })
    elephant_count = ast.literal_eval(r.text)['Number of elephants']
    print('Number of elephants found', elephant_count)

    return value
