
import json, os, csv, shutil
import pandas as pd

def check_urls_in_csv(json_directory, csv_filepath):
    """
    Checks if URLs from JSON files in a directory exist in a column of a CSV file,
    and adds a new column with the associated JSON filename.
    """

    processed_files = set()
    urls_found = set()
    url_to_filename = {}

    try:
        # open csv and get all values from Website URL row
        with open(csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            urls_from_csv = set()
            rows = []
            for row in reader:
                if row:
                    urls_from_csv.add(row[0])
                    rows.append(row)

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filepath}' not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    for filename in os.listdir(json_directory):
        if filename.endswith(".json"):
            json_filepath = os.path.join(json_directory, filename)

            if json_filepath in processed_files:
                continue  # Skip already processed files

            try:
                with open(json_filepath, 'r', encoding='utf-8') as jsonfile:
                    data = json.load(jsonfile)
                    url_from_json = data.get("url")

                    if url_from_json:
                        if url_from_json in urls_from_csv:
                            urls_found.add(url_from_json)
                            url_to_filename[url_from_json] = filename  # Store the mapping
                        else:
                            print(f"URL '{url_from_json}' from '{filename}' not found in the CSV.")
                    else:
                        print(f"URL not found in '{filename}'.")

            except FileNotFoundError:
                print(f"Error: JSON file '{json_filepath}' not found.")
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format in '{filename}'.")
            except Exception as e:
                print(f"An error occurred while processing '{filename}': {e}")

            processed_files.add(json_filepath)

    # Write the updated CSV with the new column
    try:
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            header.append("JSON Filename")  # Add the new header
            writer.writerow(header)

            for row in rows:
                url = row[0]
                if url in url_to_filename:
                    row.append(url_to_filename[url])  # Add the filename
                else:
                    row.append("ERROR")  # Add an empty string if no filename found
                writer.writerow(row)

    except Exception as e:
        print(f"An error occurred while writing the CSV file: {e}")
        return

    print(f"\nTotal unique urls from CSV: {len(urls_from_csv)}")
    print(f"Total urls found in CSV from JSON files: {len(urls_found)}")
    not_found_urls = urls_from_csv.difference(urls_found)
    if not_found_urls:
        print("\nThe following urls from the csv were not found in any json files:")
        for url in not_found_urls:
            print(f"{url}")
    else:
        print("All urls from the csv were found in the provided json files")


def copy_json_files(csv_file, source_dir, destination_dir):
    """
    Reads a CSV file, finds JSON files based on the 'JSON Filename' column,
    and copies them to a new directory.

    Args:
        csv_file (str): Path to the CSV file.
        source_dir (str): Path to the directory containing the JSON files.
        destination_dir (str): Path to the directory where JSON files should be copied.
    """

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_file}' is empty.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    if 'JSON Filename' not in df.columns:
        print("Error: 'JSON Filename' column not found in the CSV file.")
        return

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    for json_filename in df['JSON Filename']:
        source_path = os.path.join(source_dir, json_filename)
        destination_path = os.path.join(destination_dir, json_filename)

        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, destination_path)  # copy2 preserves metadata
                print(f"Copied '{json_filename}' to '{destination_dir}'")
            except Exception as e:
                print(f"Error copying '{json_filename}': {e}")
        else:
            print(f"Warning: JSON file '{json_filename}' not found in '{source_dir}'")


def check_and_log_missing_files(csv_file, destination_dir, log_file):
    """
    Checks if JSON files listed in a CSV exist in a given directory,
    and logs missing filenames to a text file.

    Args:
        csv_file (str): Path to the CSV file.
        destination_dir (str): Path to the directory where JSON files should be located.
        log_file (str): Path to the text file to log missing filenames.
    """

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file '{csv_file}' is empty.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    if 'JSON Filename' not in df.columns:
        print("Error: 'JSON Filename' column not found in the CSV file.")
        return

    missing_files = []
    for json_filename in df['JSON Filename']:
        file_path = os.path.join(destination_dir, json_filename)
        if not os.path.exists(file_path):
            missing_files.append(json_filename)

    if missing_files:
        with open(log_file, 'w') as f:
            for filename in missing_files:
                f.write(filename + '\n')
        print(f"Missing files logged to '{log_file}'.")
    else:
        print("All files found in the destination directory.")


csv_file = 'login.csv'  
source_dir = 'Finished' 
destination_dir = 'Login CSVs' 
log_file = 'missing_json_files.txt'

check_and_log_missing_files(csv_file, destination_dir, log_file)

#copy_json_files(csv_file, source_dir, destination_dir)
#check_urls_in_csv(json_directory, csv_filepath)