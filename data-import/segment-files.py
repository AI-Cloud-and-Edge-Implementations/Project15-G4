import os
from pydub import AudioSegment


for filepath in os.listdir('data'):
    print(f'Processing {filepath}...')
    file = AudioSegment.from_wav('data/' + filepath)

    segment = file[0:1]

    segment.export('segments/segment.wav', format='wav')
    print(f'Found segment of {segment.duration_seconds} seconds, exported to segments folder.')
