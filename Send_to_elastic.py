import requests
import json
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime

def send_ndjson_to_elasticsearch(file_path, es_ip, index_name, username, password):
    """
    Sends an NDJSON file to Elasticsearch over HTTPS with basic authentication.
    
    :param file_path: The path to the NDJSON file.
    :param es_ip: The Elasticsearch IP address (including port 9200).
    :param index_name: The name of the index in Elasticsearch.
    :param username: The Elasticsearch username.
    :param password: The Elasticsearch password.
    """
    es_url = f"{es_ip}/{index_name}/_bulk"
    
    # Read the NDJSON file
    with open(file_path, 'r') as file:
        ndjson_data = file.read()

    # Add header metadata for each line (required for bulk upload in Elasticsearch)
    bulk_data = ""
    for line in ndjson_data.splitlines():
        bulk_data += '{"index":{}}\n'  # Adds the indexing action for each document
        bulk_data += line + "\n"

    # Send the data to Elasticsearch
    headers = {'Content-Type': 'application/x-ndjson'}
    try:
        response = requests.post(es_url, data=bulk_data, headers=headers, 
                                 auth=HTTPBasicAuth(username, password), verify=False)  # Disable SSL verification
        response.raise_for_status()
        print(f"Data successfully sent to Elasticsearch index: {index_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data to Elasticsearch. Error: {e}")
        return False
    
    return True

def create_index_pattern(kibana_ip, index_name, username, password):
    """
    Creates an index pattern in Kibana for the specified index.
    
    :param kibana_ip: The Kibana IP address (including port).
    :param index_name: The name of the index in Elasticsearch.
    :param username: The Kibana username.
    :param password: The Kibana password.
    """
    kibana_url = f"{kibana_ip}/api/saved_objects/index-pattern"
    headers = {
        'kbn-xsrf': 'true',
        'Content-Type': 'application/json'
    }
    index_pattern_body = {
        "attributes": {
            "title": index_name + "*",  # Using wildcard for index pattern
            "timeFieldName": "@timestamp"  # Change this to your time field if different
        }
    }
    
    try:
        response = requests.post(kibana_url, headers=headers, json=index_pattern_body,
                                 auth=HTTPBasicAuth(username, password), verify=False)  # Disable SSL verification
        response.raise_for_status()
        print(f"Index pattern created successfully in Kibana: {index_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create index pattern in Kibana. Error: {e}")

def main():
    # Define the path to the NDJSON file and Elasticsearch details
    file_path = '/home/amna/Desktop/FYP_BACKEND/Model_predictions/all_predictions.ndjson'  # Path to your NDJSON file
    es_ip = 'https://127.0.0.1:9200'  # Replace with your Elasticsearch IP (including port 9200)
    kibana_ip = 'https://127.0.0.1:443'  # Use port 443 for Kibana
    index_name = f"predictions_index_{datetime.now().strftime('%Y%m%d_%H%M%S')}"  # Dynamic index name
    username = 'elastic'  # Replace with your Elasticsearch username
    password = 'UtQwHz17xAR7T6p1XazK'  # Replace with your Elasticsearch password
    
    # Send the NDJSON file to Elasticsearch
    if send_ndjson_to_elasticsearch(file_path, es_ip, index_name, username, password):
        # Create an index pattern in Kibana
        create_index_pattern(kibana_ip, index_name, username, password)

if __name__ == "__main__":
    main()
