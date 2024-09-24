import pandas as pd
import os
import numpy as np

# Define the mapping of old feature names to new feature names
feature_mapping = {
    'Src Port': 'Source Port',
    'Fwd Pkt Len Max': 'Fwd Packet Length Max',
    'TotLen Fwd Pkts': 'Total Length of Fwd Packets',
    'Flow Byts/s': 'Flow Bytes/s',
    'Init Fwd Win Byts': 'Init_Win_bytes_forward',
    'Dst Port': 'Destination Port',
    'Protocol': 'Protocol',
    'Flow Duration': 'Flow Duration',
    'Fwd Pkt Len Std': 'Fwd Packet Length Std',
    'Flow Pkts/s': 'Flow Packets/s'
}

def preprocess_csv(csv_file_path, output_folder):
    try:
        # Load the CSV data
        df = pd.read_csv(csv_file_path)
        print(f"Loaded CSV file: {csv_file_path}")
        
        # Extract Src IP, Dst IP, and Timestamp
        aux_df = df[['Src IP', 'Dst IP', 'Timestamp']].copy()
        
        # Rename the columns in the DataFrame using the mapping
        df = df.rename(columns=feature_mapping)
        
        # Reorder the columns for model input (excluding Src IP, Dst IP, and Timestamp)
        df = df[['Source Port', 'Fwd Packet Length Max', 'Total Length of Fwd Packets', 'Flow Bytes/s', 
                 'Init_Win_bytes_forward', 'Destination Port', 'Protocol', 'Flow Duration', 
                 'Fwd Packet Length Std', 'Flow Packets/s']]
        
        # Replace infinite values with NaN
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        # Fill NaN values with the mean of each column
        df.fillna(df.mean(), inplace=True)
        
        # Remove records with duplicate values
        df = df.drop_duplicates()
        
        # Remove records with null values (after filling NaNs)
        df = df.dropna()
        
        # Eliminate features with all zero values
        zero_value_columns = df.columns[(df == 0).all()]
        df = df.drop(columns=zero_value_columns)
        
        # Save the preprocessed DataFrame (for model input)
        preprocessed_file_path = os.path.join(output_folder, os.path.basename(csv_file_path))
        df.to_csv(preprocessed_file_path, index=False)
        
        # Save the auxiliary DataFrame (Src IP, Dst IP, and Timestamp)
        aux_file_path = preprocessed_file_path.replace('.csv', '_aux.csv')
        aux_df.to_csv(aux_file_path, index=False)
        
        print(f"Preprocessed CSV saved to: {preprocessed_file_path}")
        print(f"Auxiliary CSV saved to: {aux_file_path}")
    except Exception as e:
        print(f"Error processing file {csv_file_path}: {e}")

def process_all_csv_files(input_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output folder ensured at: {output_folder}")
    
    # Loop through all .csv files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            csv_file_path = os.path.join(input_folder, filename)
            print(f"Processing file: {csv_file_path}")
            preprocess_csv(csv_file_path, output_folder)
        else:
            print(f"Skipping non-CSV file: {filename}")

if __name__ == "__main__":
    # Define the paths
    input_folder = '/home/amna/Desktop/FYP_BACKEND/CICFlowmeter/bin/outputs'  # Folder with CSV files
    output_folder = '/home/amna/Desktop/FYP_BACKEND/Preprocessed_CSV' # Folder for preprocessed files
    
    process_all_csv_files(input_folder, output_folder)
