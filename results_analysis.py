import json
import os

# change source path also
source_path = "./Cleaned JSON/Failed/WCAG A/"
violation_counts = {}
severity_counts = {}
items = os.listdir(source_path)

def process_severity(json_file_path, severity_counts):
  """
  Processes a list of violations and updates the severity counts dictionary.

  Args:
    json_file_path: The path to the .JSON file.
    severity_counts: A dictionary where keys are severity IDs and values are their counts.
  """
  with open(json_file_path) as f:
    data = json.load(f)
    violations = data.get("violations", [])

    for violation in violations:
        impact_id = violation.get("impact")
        severity_counts[impact_id] = severity_counts.get(impact_id, 0) + 1


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
        # remove other not in tags for just wcag2aa
        if ('wcag2a' not in tags) and ('wcag2aa' not in tags):
            continue
        else:  
            violation_counts[violation_id] = violation_counts.get(violation_id, 0) + 1



# change this to different functions
for i in range(len(items)):
    process_severity(source_path+items[i], severity_counts)

    with open('severity_report1.txt', 'w+') as report_file:
        for violation_id, count in severity_counts.items():
            report_file.write(f"{violation_id}: {count}\n")
