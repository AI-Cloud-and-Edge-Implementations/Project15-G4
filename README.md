[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Microsoft-Project-15-Team-4
Microsoft project 15 - Team 4 solution

# Elephant Counter

## Introduction
This library predicts the number of elephants in a sound file.
The code is the deliverable of a project for the [Artificial Intelligence: Cloud and Edge Implementations](https://www.conted.ox.ac.uk/courses/artificial-intelligence-cloud-and-edge-implementations) course at the University of Oxford.

As part of [Microsoft Project 15](https://microsoft.github.io/project15/), and the [Elephant Listening Project](https://elephantlisteningproject.org/) of Cornell University,
the development team received the challenge of counting the number of elephants in a sound file.

## Documentation and Results
The explanation and results of this research project are captured in the presentation [(PowerPoint)](Project%2015%20Group%204.pptx) [(PDF)](Project%2015%20Group%204.pdf) in this repo.
There is also a [Video](TODO) explaining the results by the project team.

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

# Team 4 
- Abhishekh Baskaran - https://www.linkedin.com/in/abhishekh-jay-baskaran-566286bb/
- Bas Geerdink - https://www.linkedin.com/in/geerdink/
- Chandan Konuri - https://www.linkedin.com/in/konuri/
- Henrietta Ridley - https://www.linkedin.com/in/henriettaridley/
- Jay Padmanabhan - https://www.linkedin.com/in/jay-padmanabhan-95274b/
- Paulo Henrique De Campos Filho - https://www.linkedin.com/in/paulohcampos/
- Vishweshwar Manthani - https://www.linkedin.com/in/vishweshwar/

# Goal
Our goal was to enable researchers to be able to count the number of elephants in the wild at a specific point in time by interpreting recorded sound files to distinguish the variances in the elephants rumbles so we could say to a good degree of accuracy how many elephants were present in the recorded time frame.

# Research
- from: Joyce H. Poole research in 1999: Signals and assessment in African elephants: evidence from playback experiments 
we were able to understand that elephants used infrasonic calls  as part of their communication and that elephants would instinctively react to different playbacks of rumbles 

This gave us the idea of exploring if a recording/playback device would help the researchers by making the elephants come closer to the recording device which in turn would make it easier for the best recordings to be done.
This idea was dropped as our goal was to count them in the wild and introducing artificial “calls/rumbles” could bring more elephants that what normally be there at at a specific point in time 

- From: Cecilia Jarne research in (2019). A method for estimation of fundamental frequency for tonal sounds inspired on bird song studies
we were able to understand a simple implementation of fundamental frequency estimation using an algorithm based on a frequency-domain approach and could be easily adapted for our task
In macro steps, the method consists of:
1. take a sound segment R(t’) and perform a sonogram with the desired resolution in time 
2. For the same sound segment, to estimate the amplitude envelope 
3. For each bin corresponding to a temporal interval or window, estimate the frequency where the intensity value is maximum
4. Save in a vector the frequencies corresponding to the maximum intensity for each temporal bin. 
5. Filter the bins with the amplitude below the threshold 

- From: Angela Stoeger  et al research in (2012). Visualizing Sound Emission of Elephant Vocalizations: Evidence for Two Rumble Production Types.
we were able to understand the different rumbles an elephant produces and how to distinguish different rumbles from a same elephant from two or more rumbles from two or more elephants
The method consisted of:
1. doing an initial Acoustic video analysis. 
2. Acoustical analysis of the identified segments of each rumble 
3. Automatic classification applying a sliding window to each sound sample

- From: O'Connell-Rodwell, C.E. et al research in (2000). Seismic properties of Asian elephant (Elephas maximus) vocalizations and locomotion. Journal of the Acoustic Society of America, 108(6), 3066-3072
we were able to learn that Elephants communicate acoustically in the 20-Hz frequency range, an effective frequency for long distance trans- mission of airborne sound waves 
Although the research was focused on measuring seismic variances, understanding the frequencies at which elephants communicate gave us a better understanding of elephant communication and their frequencies
It also gave us an idea that by using seismic sensors we would be able not only to count the elephants but also predict the approximate distance they were from the monitoring station

- From: Heffner, R. S., & Heffner, H. E. (1982). Hearing in the elephant (Elephas maximus): Absolute sensitivity, frequency discrimination, and sound localization. Journal of Comparative and Physiological Psychology, 96(6), 926–944
we were able to better understand the limits of high frequency and low frequency hearing in  mammals which helped us solidify the knowledge of which frequency ranges we should focus on while trying to identify the elephant rumbles


# Literature
- Poole, Joyce H. (1999). Signals and assessment in African elephants: evidence from playback experiments. Animal Behaviour, 58(1), 185-193
- Jarne, Cecilia (2019). A method for estimation of fundamental frequency for tonal sounds inspired on bird song studies. MethodX, 6, 124-131
- Stoeger, Angela S. et al (2012). Visualizing Sound Emission of Elephant Vocalizations: Evidence for Two Rumble Production Types.
- O'Connell-Rodwell, C.E. et al (2000). Seismic properties of Asian elephant (Elephas maximus) vocalizations and locomotion. Journal of the Acoustic Society of America, 108(6), 3066-3072
- Heffner, R. S., & Heffner, H. E. (1982). Hearing in the elephant (Elephas maximus): Absolute sensitivity, frequency discrimination, and sound localization. Journal of Comparative and Physiological Psychology, 96(6), 926–944

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
- Dependency: azcopy package: https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10
```bash
foo@bar:~ docker exec -it ecc flask data_import copy_data_from_azure {source_file} {target_loc}
```
- e.g:
```bash
foo@bar:~ flask data_import copy_data_from_azure elephant-sound-data TrainingSet/nn01b elephantcallscounter/data/segments/TrainingSet/
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
  
## Project Structure:
```bash
project
│
├───docker ( The docker files)
│
├───documentation ( Documentation files )
│
├───researchanddevelopment ( R&D work )
│
├───elephantcallscounter ( Parent repository for the package )
    |
    ├── adapters (Interface for talking to external services)
    |
    ├── application (Core logic for flask api)
    |
    ├── binaries (Model files)
    |
    ├── common (Constants/ Enums and common interfaces)
    |
    ├── config (Config files environment variables parsers)
    |
    ├── data (Data for application)
    |
    ├── data_analysis (Code to generate spectrograms and boxing algorithms)
    |
    ├── data_import (Code to get data from azure and other services.)
    |
    ├── data_processing (Data processing like segmentation, thresholding, metadata processing etc)
    |
    ├── data_transformations (Filters and other data transforms)
    |
    ├── data_visualizations (Visualization tools)
    |
    ├── iot (Iot hub interface and edge code.)
    |
    ├── management (Commands and entry points)
    |
    ├── models (Neural network model code)
    |
    ├── tests (Integration and Unit tests)
    |
    ├── utils (Utility tools)
    |
    | __main__.py (application entrypoint)
    | __init__.py (db and migration utilities initializer)
    | app_factory.py(Entry point for flask app)
|   .gitignore (The files to ignore by git)
│   .env (Env file for the the .)
|   README.md ( This readme file)
|   requirements.txt ( Python packages required packages in order to run this project )
```

  
## Contribution
If you want to contribute, reach out to one of the developers, or the Project 15 team.
