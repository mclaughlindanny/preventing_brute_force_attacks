# Danny McLaughlin
# Evaluation of Machine Learning Algorithms for 
# Preventing Brute Force Attack

from preprocess_data import *
from algorithms import *

# Create dataset - file should be in csv format
filename = "./brute_force_data.csv"
final_dataset = create_dataset(filename)

# Perform feature engineering and preprocessing
final_dataset = feature_engineering(final_dataset)
final_dataset = preprocessing(final_dataset)

# Remove the labels from the dataset and 
final_y = final_dataset.pop('brute_force').values
final_y = final_y.astype('int')

# Evaluate a chosen algorithm on the generated dataset
choose_algorithm(final_dataset, final_y)


