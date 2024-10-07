import json
import os

source_path = "./Cleaned JSON/Failed/WCAG AA/"
violation_counts = {}
items = os.listdir(source_path)


def process_violations(json_file_path, violation_counts):
  """
  Processes a list of violations and updates the violation counts dictionary.

  Args:
    json_file_path: The path to the .JSON file.
    violation_counts: A dictionary where keys are violation IDs and values are their counts.
  """
  with open(json_file_path) as f:
    data = json.load(f)
    violations = data.get("violations", [])

    for violation in violations:
        violation_id = violation.get("id")

        tags = violation.get("tags")
        if ('wcag2a' not in tags) and ('wcag2aa' not in tags):
            continue
        else:  
            violation_counts[violation_id] = violation_counts.get(violation_id, 0) + 1


for i in range(len(items)):
    process_violations(source_path+items[i], violation_counts)

    with open('violations_report2.txt', 'w+') as report_file:
        for violation_id, count in violation_counts.items():
            report_file.write(f"{violation_id}: {count}\n")


print(violation_counts)