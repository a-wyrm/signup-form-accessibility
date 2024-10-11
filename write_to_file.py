import os
import csv

def list_files_to_csv(folder_path, csv_file_path):
    """Lists all files in a folder and writes them to a CSV file."""

    with open(csv_file_path, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['website'])
        for website in os.listdir(folder_path):
            name = website.split("_")
            writer.writerow([name[0]])

if __name__ == "__main__":
    folder_path = './Cleaned JSON/Failed/WCAG AA'
    csv_file_path = 'website_list3.csv'
    list_files_to_csv(folder_path, csv_file_path)