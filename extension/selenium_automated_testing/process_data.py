import os, csv
import pandas as pd

# get extension path
dir_path = os.getcwd()
extension_dir = os.path.join(dir_path, 'extension', 'selenium_automated_testing', 'retested_signups.csv')
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


create_separate()