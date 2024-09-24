import os
import subprocess
import time

def start_tshark():
    # Define the output directory inside 'media/pcaps'
    output_dir = '/home/amna/Desktop/FYP_BACKEND/CICFlowmeter/bin/inputs'

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Full path to the Tshark executable
    tshark_path = '/usr/bin/tshark'  # Typical path for Tshark on Ubuntu

    # Set the network interface (You need to specify the correct interface name)
    interface = 'ens33'  # Example: replace with your actual interface name from `tshark -D`

    file_size_limit = 5120  # 5MB limit per file
    file_count_limit = 50  # Maximum of 50 files
    capture_duration = 90  # 90 seconds capture duration

    # Infinite loop to continuously capture packets
    while True:
        timestamp = int(time.time())  # Timestamp to ensure unique file names
        output_file = os.path.join(output_dir, f'capture_{timestamp}.pcap')

        # Tshark command for rotating files based on size and time duration
        tshark_command = [
            tshark_path,
            '-i', interface,
            '-b', f'filesize:{file_size_limit}',
            '-b', f'files:{file_count_limit}',
            '-a', f'duration:{capture_duration}',
            '-w', output_file,
            '-F', 'pcap'
        ]
        
        try:
            # Start Tshark capture process in the background
            subprocess.Popen(tshark_command)
            print(f"Tshark started, capturing packets on interface {interface} to: {output_file}")
        except Exception as e:
            print(f"Error starting Tshark: {e}")
        
        # Wait for the duration before restarting capture
        time.sleep(capture_duration)

if __name__ == "__main__":
    start_tshark()

