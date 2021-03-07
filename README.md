# Microsoft-Project-15-Team-4
Microsoft project 15 - Team 4 solution

# Flask APP:
- To run the code outside docker just skip the 'docker exec -it ecc' part.
- To run the app.
```bash
foo@bar:~ flask run
```
- To run the migrations:
```bash
foo@bar:~ flask db upgrade --directory elephantcallscounter/application/persistence/migrations
```

# Build the docker container:
```bash
foo@bar:~ docker-compose up --build
```

# Docker commands to run different components:
- ecc is the container name. 
- Run these commands from another terminal.
  
## Data Import Commands:
- The following commands copy using azcopy.
- To copy data from azure. 
```bash
foo@bar:~ docker exec -it ecc flask data_import copy_data_from_azure {source_file} {target_loc}
```
- To copy data to azure.
```bash
foo@bar:~ docker exec -it ecc flask data_import copy_data_to_azure {source_file} {target_loc}
```

## Data Analysis Commands:
- To run the model:
```bash
foo@bar:~ docker exec -it ecc flask data_analysis train_cnn data/spectrogram_bb {model_name}
```

## Event Commands:
- To run the device simulator:
```bash
foo@bar:~ docker exec -it ecc flask events device_simulator elephant-sound-data realtimequeue realtimeblobs
```

## Data Processing Commands:
- To create file segments based of the filename of the metadata csv file:
```bash
foo@bar:~ docker exec -it ecc flask data_processing generate_file_segments data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt
```
- To generate the training/valid/test data based on preprocessed images:
```bash
foo@bar:~ docker exec -it ecc flask data_processing generate_training_data data/spectrogram_bb
```

## Demo Run:
- Run the db migration as specified above ^.
- Run the flask app ^.
- Run this command to start the device simulator:
```bash
foo@bar:~ flask events device_simulator tests/test_fixtures/ elephant-sound-data realtimequeue realtimeblobs 
```
- Open the browser and browse to this location: 
http://0.0.0.0:5000/elephants/elephants_count/?start_time=2020-01-10%2006:30:23&end_time=2021-01-11%2006:30:23
# Elephant Counter

## Introduction
This library predicts the number of elephants in a sound file.
The code is the deliverable of a project for the [Artificial Intelligence: Cloud and Edge Implementations](https://www.conted.ox.ac.uk/courses/artificial-intelligence-cloud-and-edge-implementations) course at the University of Oxford.

As part of [Microsoft Project 15](https://microsoft.github.io/project15/), and the [Elephant Listening Project](https://elephantlisteningproject.org/) of Cornell University,
the development team received the challenge of counting the number of elephants in a sound file.

## Literature and References
* https://elephantlisteningproject.org/
* https://azure.microsoft.com/en-us/resources/videos/project-15/
* http://ceciliajarne.web.unq.edu.ar/investigacion/

## Architecture
This library is essentially a data pipeline that consists of five main steps:
1. segmenting data: based on metadata files that is created by Cornell University, 
   we create segments of a few seconds that contain 'interesting information'
2. spectrograms: each data segment is transformed into a 2D image of time vs frequency, a `spectrogram`
3. monochrome: each spectrogram is reduced of noise and transformed into a simple monochrome (black and white) image
4. contours detection: each monochrome image is evaluated with a contour detection algorithm, to distinguish the separate 'objects' which in our case are the elephant rumbles
5. boxing: for each contour (potential elephant rumble) we calculate the size (height and width) by drawing a box around the contour
6. counting: we compare the boxes that identify the rumbles to each other in each spectrogram. Based on a few business rules, we count the number of unique elephant rumbles in each image

## Data
The raw data consists of sound files (`.wav` format) of 24 hours.
Each file is the recording of one day of sounds from a location in Africa.

## Usage
The `__main__.py` file serves as the starting point for the software.
It expects a command-line argument as a parameter, that contains the instructions.
The pipeline can be run on an entire dataset by using `full_cycle` as entry point parameter.
It's also possible to analyze one single sound file by starting at the `create_segments` or `analyse_audio_data` method.

## Contribution
If you want to contribute, reach out to one of the developers, or the Project 15 team.
There is plenty of work to do, for example:
- integration with IoT platform (e.g. Microsoft IoT Hub)
- machine learning
- other animal detection
