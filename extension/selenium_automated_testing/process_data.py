import os, csv
import pandas as pd

# get extension path
dir_path = os.getcwd()
extension_dir = os.path.join(dir_path, 'extension', 'selenium_automated_testing', 'test_signup.csv')
df = pd.read_csv(extension_dir, usecols = ['Status'])

def create_separate():
    output_dir = os.path.join(dir_path, 'output_csvs')
    os.makedirs(output_dir, exist_ok=True)


    sign_up_str = "{""isLogin"":false,""isSignup"":true,"'sendMessage'":true}"
    login_str = "{""isLogin"":true,""isSignup"":false,"'sendMessage'":true}"


    sign_up = []
    login = []
    other_df = []

    with open(extension_dir, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for url in df['Status']:
            print(url)
            try:

                if url == sign_up_str:
                    sign_up.append(url)
                elif url == login_str:
                    login.append(url)
                else:
                    other_df.append(url)
            except ValueError:
                continue
                #print(f"Skipping invalid row: {row}")
    

    #sign_up.to_csv(os.path.join(output_dir, 'sign_up_urls.csv'), index=False)
    #login.to_csv(os.path.join(output_dir, 'login_urls.csv'), index=False)


create_separate()