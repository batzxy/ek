#!/usr/bin/python3
import argparse
import json
import requests
from datetime import datetime

# Define Elasticsearch URL as a variable
elasticsearch_url = "http://127.0.0.1:9200"  # change this as per your requirement

def parse_date(date_str):
    """
    Convert date string to "YYYY-MM-DD" format.

    Args:
    date_str (str): Date string in "MM/DD/YYYY" or "YYYY-MM-DD" format.

    Returns:
    str: Date string in "YYYY-MM-DD" format or None on error.
    """
    date_formats = ["%m/%d/%Y", "%Y-%m-%d"]

    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
        except ValueError:
            pass

    print(f"Date format error for: {date_str}")
    return None

def send_to_elasticsearch(json_file_path, es, index_name):
    """
    Send JSON Lines data to Elasticsearch using Bulk API.

    Args:
    json_file_path (str): Path to JSON Lines file.
    es (str): Elasticsearch instance URL.
    index_name (str): Elasticsearch index name.
    """
    # Prepare headers for Elasticsearch
    headers = {'Content-Type': 'application/x-ndjson'}

    # Open the JSON Lines file
    with open(json_file_path, 'r') as json_file:
        bulk_data = ""
        
        # Read each line (each document) and format it for bulk indexing
        for line in json_file:
            document = json.loads(line)
            
            # Convert the date to "YYYY-MM-DD" format
            if "Date" in document:
                document["Date"] = parse_date(document["Date"])
            
            # Add a header for each document
            bulk_data += json.dumps({"index": {"_index": index_name}}) + '\n'
            # Add the document itself
            bulk_data += json.dumps(document) + '\n'

    # Send the data to Elasticsearch bulk API
    response = requests.post(f"{es}/_bulk", headers=headers, data=bulk_data)
    
    # Check for errors
    if response.status_code == 200:
        print("Data successfully indexed to Elasticsearch.")
    else:
        print(f"Failed to index data. Status code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Send a JSON Lines file to Elasticsearch using the Bulk API.")
    parser.add_argument("json_file", help="The path to the input JSON Lines file.")
    parser.add_argument("index_name", help="The name of the Elasticsearch index to which data will be posted.")

    # Parse arguments
    args = parser.parse_args()

    # Use the predefined Elasticsearch URL
    send_to_elasticsearch(args.json_file, elasticsearch_url, args.index_name)
