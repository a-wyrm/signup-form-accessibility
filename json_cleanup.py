import json
import os


def remove_inapplicable(source_file, destination_folder):

  with open(source_file, "r") as f:
    data = json.load(f)
    del data["inapplicable"]  # Remove the inapplicable section
    del data["incomplete"]
    del data["testEnvironment"]

  # Get the filename without extension
  filename = source_file.split("/")[-1].split(".")[0]
  destination_file = f"{destination_folder}/{filename}_cleaned.json"

  # Copy the modified data to a new file
  with open(destination_file, "w") as f:
    json.dump(data, f, indent=4)

  print(f"Copied and modified file saved to: {destination_file}")


source_path = "./JSON"
destination_folder = "./JSON cleaned"
#source_path = "path/to/your/source.json"
items = os.listdir(source_path)
for i in range(len(items)):
    print(items[i])
    remove_inapplicable("./JSON/"+items[i], destination_folder)