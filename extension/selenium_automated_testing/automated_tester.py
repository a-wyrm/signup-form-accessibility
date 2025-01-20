from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os
import pandas as pd
from selenium.webdriver.chrome.service import Service


# get extension path
dir_path = os.getcwd()
extension_dir = os.path.join(dir_path, 'extension', 'dist') 

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("load-extension=" + extension_dir)
options.add_argument("--no-sandbox")
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
sign_up_url_path = os.path.join(dir_path, 'extension', 'selenium_automated_testing', 'signup_urls.csv') 
df = pd.read_csv(sign_up_url_path, usecols = ['Signup'])


def activate_extension():
    driver.get('chrome-extension://'+extension_id+'/popup.html')

for url in df['Signup']:
    driver.get(url)
    driver.implicitly_wait(10)
driver.quit()
