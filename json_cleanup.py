import json
import os
import csv

def remove_inapplicable(source_file, destination_folder):

  with open(source_file, "r") as f:
    data = json.load(f)
    del data["inapplicable"]
    del data["incomplete"]
    del data["testEnvironment"]

  # Get the filename without extension
  filename = source_file.split("/")[-1].rsplit('.', 1)[0]
  destination_file = f"{destination_folder}/{filename}_cleaned.json"

  # Copy the modified data to a new file
  with open(destination_file, "w") as f:
    json.dump(data, f, indent=4)

def check_violations(json_file_path, target_path1, target_path2):
  with open(json_file_path) as f:
    data = json.load(f)
    filename = json_file_path.split("/")[-1].rsplit('.', 1)[0]

    # Check if "violations" key exists and is empty
    if len(data['violations']) == 0:
        destination_file = f"{target_path1}/{filename}.json"
        with open(destination_file, "w") as f:
          json.dump(data, f, indent=4)
    else:
      destination_file = f"{target_path2}/{filename}.json"
      with open(destination_file, "w") as f:
        json.dump(data, f, indent=4)
                  

def count_violations(json_file_path, file_name, csv_file_path):
    """Count violations in file."""
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        name = file_name.split("_")
        with open(json_file_path) as f:
            data = json.load(f)
            length = len(data['violations'])
            writer.writerow([name[0], length])

    
source_path = "./Processed Data/Cleaned JSON/Failed/WCAG AA/"
destination_folder1 = "./Passed"
destination_folder2 = "./Failed"
items = os.listdir(source_path)

for i in range(len(items)):
    #remove_inapplicable(source_path+items[i], "./Cleaned JSON/")
    csv_file_path = 'violation_list1.csv'
    count_violations(source_path+items[i], items[i], csv_file_path)