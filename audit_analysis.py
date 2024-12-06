import os
import csv

csv_data = ["Website Name", "Error", "Number of Errors"]

def audit_checker(json_file_path):
    with open(json_file_path, 'r', newline='') as csvfile:
        violations_dict = {}
        reader = csv.reader(csvfile)
        first_column = [row[0] for row in reader]

        file_name = ((json_file_path.split('/'))[-1]).split('.')[0]
        
        for i in range(len(first_column)):
            print(first_column[i])
            #index = first_column[i].find(':')
            if('Other issues:' not in first_column[i]):
                violations_dict[first_column[i]] = violations_dict.get(first_column[i], 0) + 1

        with open(file_name+'.csv', 'w+', newline='') as report_file:
            writer = csv.DictWriter(report_file, fieldnames=csv_data)
            writer.writeheader()
            for violation_id, count in violations_dict.items():
                writer.writerow({'Website Name': file_name, 'Error': violation_id, 'Number of Errors': count})

               

#source_path = "./Full Accessibility Audit/"
source_path = "./Text Reports/"
items = os.listdir(source_path)

for i in range(len(items)):
    audit_checker(source_path+items[i])