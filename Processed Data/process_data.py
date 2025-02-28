import os, json, shutil, re
import numpy as np
import pandas as pd

# get extension path
dir_path = os.getcwd()
extension_dir = os.path.join(dir_path, 'Processed Data', 'sign_up_final.csv')
df = pd.read_csv(extension_dir, usecols = ['Website', 'Status'])

def create_separate():
    output_dir = os.path.join(dir_path, 'output_csvs')
    os.makedirs(output_dir, exist_ok=True)


    sign_up_str = "True"
    login_str = "False"
    retest_str = "No data"

    sign_up = []
    login = []
    retest = []
    other_df = []

    for i, row in df.iterrows():
        website = row['Website']
        status = row['Status']
        try:
            if status == sign_up_str:
                sign_up.append([website, status])
            elif status == login_str:
                login.append([website, status])
            elif status == retest_str:
                retest.append([website, status])
            else:
                other_df.append([website, status])
        except ValueError:
            print(f"Skipping invalid row: {website}, {status}")


    sign_up_df = pd.DataFrame(sign_up, columns=['Website', 'Status'])
    login_df = pd.DataFrame(login, columns=['Website', 'Status'])
    retest_df = pd.DataFrame(retest, columns=['Website', 'Status'])
    other_df = pd.DataFrame(other_df, columns=['Website', 'Status'])

    sign_up_df.to_csv(os.path.join(output_dir, "sign_up_retested.csv"), index=False)
    login_df.to_csv(os.path.join(output_dir, "login_retested.csv"), index=False)
    retest_df.to_csv(os.path.join(output_dir, "no_data_urls.csv"), index=False)
    other_df.to_csv(os.path.join(output_dir, "other_retested.csv"), index=False)


dict_to_walk = os.path.join(dir_path, 'Processed Data', 'Cleaned JSON', 'Failed', "WCAG A")

def valid_signups():

    # Create folder
    if not os.path.exists("Filtered Sign Up Audits"):
        os.makedirs("Filtered Sign Up Audits")

    to_array = df['Website'].to_numpy()
    check_diff = []
    for root, _, files in os.walk(dict_to_walk):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as jsonfile:
                        audit_data = json.load(jsonfile)
                        if 'url' in audit_data and audit_data['url'] in to_array:
                            """ output_file_path = os.path.join("Filtered Sign Up Audits", file)
                            shutil.copy2(file_path, output_file_path)
                            print(f"Copied: {file}") """
                            check_diff.append(audit_data['url'])

                except FileNotFoundError:
                    print(f"Warning: File not found {file}")
    
    diff = np.setdiff1d(to_array, check_diff)
    data_d = pd.DataFrame(diff, columns=['Values'])
    data_d.to_csv("difference", index=False)


def edit_sting(url):
    url_name = url

    if url_name.startswith("http://"):
        url_name = url_name[7:]
    elif url_name.startswith("https://"):
        url_name = url_name[8:]
    if url_name.startswith("www."):
        url_name = url_name[4:]

    last_dot_index = url_name.find(".")
    url_name = url_name[:last_dot_index]

    return url_name

def get_diff_audits(directory):

    for x in directory['Values']:
        link_name = edit_sting(x)
        #print(link_name)

        for root, _, files in os.walk(dict_to_walk):
            for file in files:
                if file.endswith('.json'):
                    # Name of file
                    file_name = edit_sting(file)

                    file_path = os.path.join(root, file)

                    if file_name == link_name:
                        output_file_path = os.path.join("Filtered Sign Up Audits", file)
                        shutil.copy2(file_path, output_file_path)
                        print(f"Copied: {file}")
                        break

difference_dir = os.path.join(dir_path, 'Processed Data', 'difference.csv')
difference_dir = pd.read_csv(difference_dir, usecols = ['Values'])
get_diff_audits(difference_dir)

#to_array = df['Website'].to_numpy()
#print(len(to_array))