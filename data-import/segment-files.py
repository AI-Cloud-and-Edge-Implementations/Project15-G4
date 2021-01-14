import os
import pandas as pd
from pydub import AudioSegment

# read metadata
metadata_filepath = 'metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
metadata = pd.read_csv(metadata_filepath, sep='\t', lineterminator='\r', header=0)

# TODO: add other metadata files?

# process raw files
for filename in os.listdir('data'):
    print(f'Processing {filename}...')
    file = AudioSegment.from_wav('data/' + filename)

    # get the relevant segments from the metadata
    metadata_segments = metadata[metadata['filename'] == filename]

    for index, metadata_segment in metadata_segments.iterrows():
        try:
            selection = metadata_segment["Selection"].lstrip()
            print(f' Generating segment {selection}...')

            start = metadata_segment['File Offset (s)']  # ms
            duration = metadata_segment['duration'] * 1000  # ms
            end = start + duration

            segment = file[start:end]

            marginal = str(metadata_segment['marginals']).strip()
            segment_path = f'segments/{filename}_segment_{selection}_{marginal}.wav'
            segment.export(segment_path, format='wav')
            print(f' Found segment of {segment.duration_seconds} seconds, exported to {segment_path}.')
        except Exception as e:
            print('  Error when creating segment: ' + str(e))
