import os
import csv
from collections import Counter

csv_data = ["Website Name", "Error", "Number of Errors"]
def check_reports(json_file_path, violations_dict):
    with open(json_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 1:
                first_column_value = row[1]
                violations_dict[first_column_value] = violations_dict.get(first_column_value, 0) + 1
        
        with open('Popular.csv', 'a', newline='') as report_file:
            writer = csv.DictWriter(report_file, fieldnames=['Website Name', "Error", "Number of Errors"])
            writer.writeheader()
            for violation_id, count in violations_dict.items():
                writer.writerow({'Website Name': items[i], 'Error': violation_id, 'Number of Errors': count})
        

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

               
def count_errors(json_file_path):
  with open(json_file_path, 'r') as f:
      column = (row[2] for row in csv.reader(f))
      print("Most frequent value: {0}".format(Counter(column).most_common()[0][0]))


#source_path = "./Full Accessibility Audit/"
source_path = "./Text Reports/Less Popular/"
items = os.listdir(source_path)

for i in range(len(items)):
    v = {}
    count_errors(source_path+items[i])

