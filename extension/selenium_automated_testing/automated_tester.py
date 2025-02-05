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
#header = ['Website URL', 'Status']

#with open('test_signup.csv', 'a', encoding='UTF8', newline='') as f:
#    writer = csv.writer(f)
#    written_data = []


def generate_csv_from_local_storage(driver, filename="local_storage_data.csv", keys_to_extract=None):
    """
    Generates a CSV file from data stored in the browser's local storage.

    Args:
        driver: A Selenium WebDriver instance.
        filename: The name of the CSV file to create (default: "local_storage_data.csv").
        keys_to_extract: A list of specific keys to extract from local storage. If None, all keys are extracted.

    Returns:
        True if the CSV file was successfully created, False otherwise.  Prints errors.
    """

    try:
        # Inject JavaScript to get local storage data.  This handles JSON stringification.
        script = """
        let data = {};
        const keys = Object.keys(localStorage);

        if (arguments[0] === null) { // Extract all if keys_to_extract is None
          keys.forEach(key => {
            try {
              const value = localStorage.getItem(key);
              // Attempt parsing JSON. If it fails, treat as a regular string.
              data[key] = JSON.parse(value);
            } catch (e) {
              data[key] = value;
            }
          });
        } else { // Extract only specified keys
            arguments[0].forEach(key => {
                try {
                  const value = localStorage.getItem(key);
                  data[key] = JSON.parse(value);
                } catch (e) {
                  data[key] = value;
                }
            });
        }

        return data;

        """

        local_storage_data = driver.execute_script(script, keys_to_extract)


        if not local_storage_data:
            print("No data found in local storage.")
            return False

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header row (keys)
            header = list(local_storage_data.keys())  # Get the keys dynamically
            writer.writerow(header)

            # Write data rows
            writer.writerow(local_storage_data.values())

        print(f"CSV file '{filename}' created successfully.")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def activate_extension():
    id_tag = 'detectedWhat'
    try:
        div_element = driver.find_element(By.ID, id_tag)
        inner_html = div_element.get_attribute("innerHTML")
        print(inner_html)
        #written_data.append(inner_html)
        #writer.writerow(written_data)
    except:
        print("Unable to get id (website likely unavailable).")
        #written_data.append('INVALID')
        #writer.writerow(written_data)
    
    #written_data.clear()

generate_csv_from_local_storage(driver)

""" for url in df['Signup']:
    try:
        driver.get(url)
        #written_data.append(url)
        time.sleep(5)
        #activate_extension()
    except WebDriverException or TimeoutException or requests.exceptions.ReadTimeout as e:
        print(f"Error {e} at {url}.")
        #written_data.append(url)
        #written_data.append('INVALID')
        #writer.writerow(written_data)
        #written_data.clear() """

driver.quit()
