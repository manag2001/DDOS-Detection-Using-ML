import pandas as pd
import joblib  # or use pickle
import os
import json

# Label mapping: from numeric to class names
label_mapping = {
    0: 'BENIGN',
    1: 'DrDoS_LDAP',
    2: 'DrDoS_NetBIOS',
    3: 'DrDoS_UDP',
    4: 'Syn',
    5: 'UDP-lag'
}

def load_model(model_path):
    # Load the trained model from a file
    return joblib.load(model_path)

def predict_with_model(model, data):
    # Perform predictions using the trained model
    return model.predict(data)

def decode_labels(predictions, label_mapping):
    # Map numeric predictions back to class names
    return [label_mapping[pred] for pred in predictions]

def save_predictions_to_ndjson(predictions_dict, output_file_path):
    # Save the dictionary as an NDJSON file
    with open(output_file_path, 'a') as f:
        for entry in predictions_dict:
            json.dump(entry, f)
            f.write("\n")

def main():
    # Define the paths
    model_path = '/home/amna/Desktop/FYP_BACKEND/Models/decision_tree_modelv3.pkl'  # Path to the saved trained model
    preprocessed_folder = '/home/amna/Desktop/FYP_BACKEND/Preprocessed_CSV'  # Folder with preprocessed CSV files
    output_file_path = '/home/amna/Desktop/FYP_BACKEND/Model_predictions/all_predictions.ndjson'  # Single file for all predictions

    # Load the trained model
    model = load_model(model_path)
    
    # Loop through all preprocessed CSV files in the folder
    for filename in os.listdir(preprocessed_folder):
        if filename.endswith(".csv") and not filename.endswith('_aux.csv'):
            csv_file_path = os.path.join(preprocessed_folder, filename)
            aux_file_path = csv_file_path.replace('.csv', '_aux.csv')
            
            # Load preprocessed data
            data = pd.read_csv(csv_file_path)
            
            # Load auxiliary data (Src IP, Dst IP, and Timestamp)
            aux_data = pd.read_csv(aux_file_path)
            
            # Perform predictions
            predictions = predict_with_model(model, data)
            
            # Decode numeric predictions to class names
            decoded_predictions = decode_labels(predictions, label_mapping)
            
            # Get the most frequent 'Src IP' and 'Dst IP'
            source_ip = aux_data['Src IP'].value_counts().idxmax()
            dest_ip = aux_data['Dst IP'].value_counts().idxmax()
            
            # Extract Timestamps from the auxiliary data
            timestamps = aux_data['Timestamp']
            
            # Create a list of dictionaries for each prediction, adding 'source_ip', 'dest_ip', and 'Timestamp'
            predictions_dict = [{"index": i, "prediction": pred, "source_ip": source_ip, 
                                 "dest_ip": dest_ip, "timestamp": timestamps.iloc[i]} 
                                for i, pred in enumerate(decoded_predictions)]
            
            # Save all predictions to a single NDJSON file
            save_predictions_to_ndjson(predictions_dict, output_file_path)
            
            # Print confirmation
            print(f"Predictions for {filename} saved to {output_file_path}")

if __name__ == "__main__":
    main()
