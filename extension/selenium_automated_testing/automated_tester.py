from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time, os, csv, requests
import pandas as pd
from selenium.webdriver.chrome.service import Service

# get extension path
dir_path = os.getcwd()
extension_dir = os.path.join(dir_path, 'extension', 'dist') 

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("load-extension=" + extension_dir)
options.add_argument("--no-sandbox")
options.add_argument('--remote-debugging-pipe')
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.get("chrome://extensions/")

# Get Extension ID
extensions_manager = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "extensions-manager")))
# Access the shadow DOM of extensions-manager
extensions_manager_shadow_root = extensions_manager.shadow_root
extensions_item_list = WebDriverWait(extensions_manager_shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "extensions-item-list")))
extensions_item_list_shadow_root = extensions_item_list.shadow_root
extensions_item = WebDriverWait(extensions_item_list_shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "extensions-item")))
# the extension ID
extension_id = extensions_item.get_attribute("id")

# Get URLS
sign_up_url_path = os.path.join(dir_path, 'extension', 'selenium_automated_testing', 'signup_urls_small.csv') 
df = pd.read_csv(sign_up_url_path, usecols = ['Signup'])


# CSV function
header = ['Website URL', 'Status']

with open('test_signup.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    written_data = []

    def activate_extension():
        id_tag = 'detectedWhat'
        try:
            div_element = driver.find_element(By.ID, id_tag)
            inner_html = div_element.get_attribute("innerHTML")
            print(inner_html)
            written_data.append(inner_html)
            writer.writerow(written_data)
        except:
            print("Unable to get id (website likely unavailable).")
            written_data.append('No data')
            writer.writerow(written_data)
        
        written_data.clear()


    for url in df['Signup']:
        try:
            driver.get(url)
            written_data.append(url)
            time.sleep(5)
            activate_extension()
        except WebDriverException or TimeoutException or requests.exceptions.ReadTimeout as e:
            print(f"Error {e} at {url}.")
            written_data.append(url)
            written_data.append('INVALID')
            writer.writerow(written_data)
            written_data.clear()


driver.quit()
