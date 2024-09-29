import json
import os


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

  #print(f"Copied and modified file saved to: {destination_file}")

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
                  
source_path = "./Cleaned JSON/"
destination_folder1 = "./Passed"
destination_folder2 = "./Failed"
items = os.listdir(source_path)

for i in range(len(items)):
    #remove_inapplicable(source_path+items[i], "./Cleaned JSON/")
    check_violations(source_path+items[i], destination_folder1, destination_folder2)