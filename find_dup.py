import os
import pandas as pd

def find_missing_json(csv_file, json_folder, csv_column='JSON Filename'):
    """
    Finds the JSON files in the folder that are not listed in the CSV file and saves them to a text file.

    Args:
        csv_file (str): Path to the CSV file.
        json_folder (str): Path to the folder containing JSON files.
        csv_column (str): The column name in the CSV containing JSON file names.

    Returns:
        list or None: A list of missing filenames, or None if no discrepancy is found.
    """

    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Extract the JSON filenames from the specified column
        csv_filenames = set(df[csv_column].tolist())

        # Get the list of JSON files from the folder
        json_files = {f for f in os.listdir(json_folder) if f.lower().endswith('.json')}

        # Find the difference between the folder files and the CSV files
        missing_files = list(json_files - csv_filenames)

        if missing_files:
            return missing_files
        else:
            return None  # No missing files found

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None
    except KeyError as e:
        print(f"Error: Column '{csv_column}' not found in CSV.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

csv_file_path = 'wcag_violations_hard copy 2.csv'  # Replace with your CSV file path
json_folder_path = 'Processed Sign Up Audits'

missing_files = find_missing_json(csv_file_path, json_folder_path)

if missing_files:
    print("Missing JSON files found. Saving to missing_files.txt...")
    with open('missing_files.txt', 'w') as f:
        for file in missing_files:
            f.write(file + '\n')
    print("Missing files saved to missing_files.txt")
else:
    print("All JSON files in the folder are accounted for in the CSV.")