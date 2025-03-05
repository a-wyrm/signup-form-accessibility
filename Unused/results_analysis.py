import json, os, csv


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


def import_violations_and_severity_to_csv(json_file_path, violation_counts, severity):
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
        severity_id = violation.get("impact")

        tags = violation.get("tags")

        # remove other not in tags for just wcag2aa
        if ('wcag2a' not in tags) and ('wcag2aa' not in tags):
            continue
        else:  
            violation_counts[violation_id] = violation_counts.get(violation_id, 0) + 1
            severity.setdefault(violation_id, severity_id)


# change source path also
dir_path = os.getcwd()
file_dir = os.path.join(dir_path, 'Filtered Sign Up Audits')
violation_counts = {}
severity = {}
severity_counts = {}
items = os.listdir(file_dir)

""" for i in range(len(items)):
    import_violations_and_severity_to_csv(file_dir+"/"+items[i], violation_counts, severity)
    with open('violations_checker.csv', 'w+', newline='') as report_file:
        fieldnames = ['Violation ID', 'Count', 'Severity']
        writer = csv.DictWriter(report_file, fieldnames=fieldnames)
        writer.writeheader()
        for violation_id, count in violation_counts.items():
            writer.writerow({'Violation ID': violation_id, 'Count': count, 'Severity': severity[violation_id]})
 """



# comment these out if you want to count violations individually
for i in range(len(items)):
    process_violations(file_dir+"/"+items[i], violation_counts)

    with open('violations_checker.txt', 'w+') as report_file:
        for violation_id, count in violation_counts.items():
            report_file.write(f"{violation_id}: {count}\n")


""" # change this to different functions
for i in range(len(items)):
    process_severity(source_path+items[i], severity_counts)

    with open('severity_report1.txt', 'w+') as report_file:
        for violation_id, count in severity_counts.items():
            report_file.write(f"{violation_id}: {count}\n") """


