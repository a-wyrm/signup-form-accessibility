from selenium import webdriver
import time, os, csv
import pandas as pd
from selenium.webdriver.chrome.service import Service


# get extension path
dir_path = os.getcwd()
extension_dir = os.path.join(dir_path, 'extension', 'dist') 

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("load-extension=" + extension_dir)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Get URLS
sign_up_url_path = os.path.join(dir_path, 'extension', 'selenium_automated_testing', 'signup_urls.csv') 
df = pd.read_csv(sign_up_url_path, usecols = ['Signup'])

# TODO: insure extension gets clicked and we get data from extension

for url in df['Signup']:
    driver.get(url)
    driver.implicitly_wait(10)
driver.quit()


#driver.maximize_window()
#time.sleep(15)