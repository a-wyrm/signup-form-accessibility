import json
import os

# remove and clean file
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
    

# script that checks if there are any violations
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
                  

def wcag_check(json_file_path):
    with open(json_file_path) as f:
        data = json.load(f)
        filename = json_file_path.split("/")[-1].rsplit('.', 1)[0]

        violations = data.get("violations")

        tag_list = []
        for violation in violations:
            tags = violation.get("tags")
            for t in tags:
                tag_list.append(t)
    
        if ('wcag2a' in tag_list):
            destination_file = f"./WCAG A/{filename}.json"
            with open(destination_file, "w") as f:
                json.dump(data, f, indent=4)
            return
        elif ('wcag2aa' in tag_list):
            destination_file = f"./WCAG AA/{filename}.json"
            with open(destination_file, "w") as f:
                json.dump(data, f, indent=4)
            return
        else:
            destination_file = f"./Best Practices/{filename}.json"
            print(filename)
            with open(destination_file, "w") as f:
                json.dump(data, f, indent=4)
            return
               

source_path = "./Cleaned JSON/Failed/"
destination_folder1 = "./Cleaned JSON/Failed/Best Practices"
destination_folder2 = "./Failed"
items = os.listdir(source_path)

for i in range(len(items)):
    #remove_inapplicable(source_path+items[i], "./Cleaned JSON/")
    #check_violations(source_path+items[i], destination_folder1, destination_folder2)
    wcag_check(source_path+items[i])