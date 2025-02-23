import os, csv, time, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

def setup_driver():
    """Sets up the Chrome WebDriver with extension and options."""
    dir_path = os.getcwd()
    extension_dir = os.path.join(dir_path, 'extension', 'dist')
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument(f"load-extension={extension_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument('--remote-debugging-pipe')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions-file-access-check")
    options.add_argument("--disable-extensions-http-throttling")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,)
    return driver

def get_extension_id(driver):
    """Retrieves the extension ID from the Chrome extensions page."""
    driver.get("chrome://extensions/")
    try:
        extensions_manager = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "extensions-manager"))
        )
        extensions_manager_shadow_root = extensions_manager.shadow_root
        extensions_item_list = WebDriverWait(extensions_manager_shadow_root, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "extensions-item-list"))
        )
        extensions_item_list_shadow_root = extensions_item_list.shadow_root
        extensions_item = WebDriverWait(extensions_item_list_shadow_root, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "extensions-item"))
        )
        return extensions_item.get_attribute("id")
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Error getting extension ID: {e}")
        return None

def load_urls(filepath):
    """Loads website URLs from a CSV file."""
    try:
        df = pd.read_csv(filepath, usecols=['Website'])
        return df['Website'].tolist()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []

def activate_extension(driver, writer, written_data):
    """Activates the extension and writes the result to the CSV."""
    id_tag = 'detectedWhat'
    try:
        div_element = driver.find_element(By.ID, id_tag)
        inner_html = div_element.get_attribute("innerHTML")
        print(inner_html)
        written_data.append(inner_html)
    except NoSuchElementException:
        print("Unable to get id (website likely unavailable).")
        written_data.append('No data')
    except Exception as e:
        print(f"An unexpected error occurred while activating the extension: {e}")
        written_data.append('Error')

    writer.writerow(written_data)
    written_data.clear()

def initial_test():
    """Performs the initial test on the loaded URLs."""
    driver = setup_driver()
    extension_id = get_extension_id(driver)

    if extension_id is None:
        driver.quit()
        return

    sign_up_url_path = os.path.join(os.getcwd(), 'extension', 'selenium_automated_testing', 'output_csvs', 'retest_urls.csv')
    urls = load_urls(sign_up_url_path)

    if not urls:
        driver.quit()
        return

    header = ['Website URL', 'Status']
    with open('retested_signups.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        written_data = []

        for url in urls:
            try:
                driver.get(url)
                written_data.append(url)
                driver.set_page_load_timeout(35)
                time.sleep(5)
                activate_extension(driver, writer, written_data)
            except (WebDriverException, TimeoutException, requests.exceptions.ReadTimeout, ConnectionResetError) as e:
                print(f"Error {e} at {url}.")
                written_data.append(url)
                written_data.append('INVALID')
                writer.writerow(written_data)
                written_data.clear()
            except Exception as e:
                print(f"An unexpected error occurred while processing {url}: {e}")
                written_data.append(url)
                written_data.append('ERROR')
                writer.writerow(written_data)
                written_data.clear()

    driver.quit()

if __name__ == "__main__":
    initial_test()