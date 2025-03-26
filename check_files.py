import json
import os
import csv

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
            print(f"    {url}")
    else:
        print("All urls from the csv were found in the provided json files")

json_directory = "Processed Sign Up Audits"
csv_filepath = "wcag_violations_hard.csv"

check_urls_in_csv(json_directory, csv_filepath)