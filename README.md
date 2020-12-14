# preventing_brute_force_attacks

# Purpose
  This application evaluates several machine learning algorithms based out of the Python sklearn library on how effectively they can distinguish a brute force log-in attempt from a failed log-in attempt from an authorized user. 

# Running the code
  The only requirement for running this application is that all the source code be in the same directory as the dataset. The dataset is given in brute_force_data.csv. From there the main file should be run and algorithms can be evaluated at the user's pleasure. 
  
# Editing the dataset
  Adding instances to the dataset can be acomplished in two ways. The csv file could be edited directly or the create_dataset method in preprocess_data.py can be edited to add more pseudo data. A new dataset can be used if it is in the same format as the current file. The filename variable will have to be changed in main.py. If new features are to be added then additional code changes will be required in preprocessing_data.py. 
