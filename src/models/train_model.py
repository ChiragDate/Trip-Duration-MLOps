# train_model.py
import os
import pathlib
import sys
import yaml
import joblib

import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def train_model(train_features, target, n_estimators, max_depth, seed):
    # Train your machine learning model
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=seed)
    model.fit(train_features, target)
    return model

def save_model(model, output_path):
    # Save the trained model to the specified output path
    joblib.dump(model, os.path.join(output_path, 'model.joblib'))

def main():
    curr_dir = pathlib.Path(__file__)
    home_dir = curr_dir.parent.parent.parent
    params_file = os.path.join(home_dir, 'params.yaml')
    print(f"Params file: {params_file}")
    params = yaml.safe_load(open(params_file))["train_model"]

    input_file = sys.argv[1]
    data_path = input_file if os.path.isabs(input_file) else os.path.join(home_dir, input_file)
    print(f"Data: {data_path}")
    
    output_path = os.path.join(home_dir, 'models')
    print(f"Output_path: {output_path}")
    
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
    
    train_csv_path = os.path.join(data_path, 'train.csv')
    print(f"train features: {train_csv_path}")
    
    train_features = pd.read_csv(train_csv_path)
    print(f"Available columns: {train_features.columns.tolist()}")
    
    # Check if the target column exists
    TARGET = 'trip_duration'
    if TARGET not in train_features.columns:
        print(f"Warning: '{TARGET}' column not found. Using the last column as target.")
        # Use the last column as target if trip_duration is not found
        TARGET = train_features.columns[-1]
        print(f"Using '{TARGET}' as target column instead.")
    
    X = train_features.drop(TARGET, axis=1)
    y = train_features[TARGET]
    
    print("Reached train model")
    trained_model = train_model(X, y, params['n_estimators'], params['max_depth'], params['seed'])
    print("model trained")
    save_model(trained_model, output_path)
    print("model saved")

if __name__ == "__main__":
    main()