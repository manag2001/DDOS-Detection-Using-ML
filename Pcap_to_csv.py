import os
import shutil
import subprocess

def convert_pcap_to_csv(pcap_folder, output_folder, cfm_script_path):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all .pcap files in the pcap_folder
    for filename in os.listdir(pcap_folder):
        if filename.endswith(".pcap"):
            pcap_file_path = os.path.join(pcap_folder, filename)
            # Output file will have the same name as the pcap file, but with a .csv extension
            output_file_name = os.path.splitext(filename)[0] + ".csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Command to run the cfm.sh with the PCAP file and output directory
            command = ['bash', cfm_script_path, pcap_file_path, output_folder]

            try:
                # Run the script and wait for it to complete
                subprocess.run(command, check=True)
                print(f"Successfully processed {filename}")

                # Check if a folder was created
                folder_created = os.path.join(output_folder, os.path.splitext(filename)[0])
                if os.path.exists(folder_created):
                    # Move the CSV file back to the main output folder
                    csv_file_created = os.path.join(folder_created, output_file_name)
                    if os.path.exists(csv_file_created):
                        shutil.move(csv_file_created, output_file_path)
                        print(f"Moved {output_file_name} to {output_folder}")
                    
                    # Remove the created folder
                    shutil.rmtree(folder_created)
                    print(f"Removed folder {folder_created}")

            except subprocess.CalledProcessError as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Define the folders and script location
    pcap_folder = '/home/amna/Desktop/FYP_BACKEND/CICFlowmeter/bin/inputs'  # Folder with PCAP files
    output_folder = '/home/amna/Desktop/FYP_BACKEND/CICFlowmeter/bin/outputs'  # Folder to save the CSV files
    cfm_script_path = '/home/amna/Desktop/FYP_BACKEND/CICFlowmeter/bin/./cfm'  # Path to the cfm.sh script
    os.chdir('/home/amna/Desktop/FYP_BACKEND/CICFlowmeter/bin')

    # Call the function to process all pcap files
    convert_pcap_to_csv(pcap_folder, output_folder, cfm_script_path)
