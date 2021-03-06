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
- Run the flask app
- Run this command to start the device simulator:
```bash
foo@bar:~ flask events device_simulator tests/test_fixtures/ elephant-sound-data realtimequeue realtimeblobs 
```
- Open the browser and browse to this location: 
http://0.0.0.0:5000/elephants/elephants_count/?start_time=2020-01-10%2006:30:23&end_time=2021-01-11%2006:30:23
