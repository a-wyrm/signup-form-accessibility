# Resources: https://blog.pamelafox.org/2023/07/automated-accessibility-audits-for.html
# https://playwright.dev/
# https://pamelafox.github.io/axe-playwright-python/

import json, os, csv
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from pathlib import Path
from urllib.parse import urlparse


cwd = Path.cwd()
axe = Axe()

with open('save.csv', newline='') as csvfile:
        with sync_playwright() as playwright:
            reader = csv.DictReader(csvfile)
            for row in reader:
                parsed_url = urlparse(row['Values'])

                browser = playwright.chromium.launch()
                page = browser.new_page()

                # Need to account for 'playwright._impl._errors.Error: Page.goto: net::ERR_EMPTY_RESPONSE' error here
                try:
                    page.goto(row['Values'])
                    results = axe.run(page)
                    results.save_to_file(cwd/'JSON/', parsed_url.netloc+'.json')
                    browser.close()
                except Exception as error:
                    with open('invalid.csv', 'a', newline='') as invalid_file:
                        writer = csv.writer(invalid_file)
                        writer.writerow([row['Values'], str(error)])
                    continue




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
               

""" source_path = "./Processed Data/Cleaned JSON/Failed/"
destination_folder1 = "./Processed Data/Cleaned JSON/Failed/Best Practices"
destination_folder2 = "./Failed"
items = os.listdir(source_path)

for i in range(len(items)):
    #remove_inapplicable(source_path+items[i], "./Cleaned JSON/")
    #check_violations(source_path+items[i], destination_folder1, destination_folder2)
    wcag_check(source_path+items[i]) """