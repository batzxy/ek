#!/usr/bin/python3
import csv
import json
import argparse

def infer_type(value):
    # Try converting to int
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try converting to float
    try:
        return float(value)
    except ValueError:
        pass

    # Return the value as a string if no other type matches
    return value

def csv_to_json_lines(csv_file_path, json_file_path):
    # Open the CSV file and initialize JSON lines format
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Prepare each row as a JSON object line with type inference
        json_lines = []
        for row in csv_reader:
            typed_row = {key: infer_type(value) for key, value in row.items()}
            json_lines.append(json.dumps(typed_row))
    
    # Write JSON lines to the output file
    with open(json_file_path, 'w') as json_file:
        json_file.write('\n'.join(json_lines))

    print(f"Successfully converted {csv_file_path} to {json_file_path} in JSON Lines format.")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert CSV to JSON Lines format with inferred types for Elasticsearch.")
    parser.add_argument("csv_file", help="The path to the input CSV file.")
    parser.add_argument("json_file", help="The path to the output JSON file.")

    # Parse arguments
    args = parser.parse_args()

    # Run the conversion
    csv_to_json_lines(args.csv_file, args.json_file)


