# Microsoft-Project-15-Team-4
Microsoft project 15 - Team 4 solution

# Build the docker container:
```bash
foo@bar:~ docker-compose up --build
```

# Docker commands to run different components:
- ecc is the container name. 
- Run these commands from another terminal.
  
## Data Import Commands:
- To copy data from azure. 
```bash
foo@bar:~ docker exec -it ecc python3 -m elephantcallscounter data_import copy_data_to_azure {source_file} {target_loc}
```

## Data Analysis Commands:
- To run the model:
```bash
foo@bar:~ docker exec -it ecc python3 -m elephantcallscounter data_analysis train_cnn data/spectrogram_bb
```

## Event Commands:
- To run the device simulator:
```bash
foo@bar:~ docker exec -it ecc python3 -m elephantcallscounter events device_simulator
```

## Data Processing Commands:
- To create file segments based of the filename of the metadata csv file:
```bash
foo@bar:~ docker exec -it ecc python3 -m elephantcallscounter generate_file_segments data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt
```