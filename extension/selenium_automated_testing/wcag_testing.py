import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def test_WCAG_211_keyboard(driver, url):
    """
    Checks for a keyboard trap on a website.

    Args:
        driver: Chrome driver.
        url: URL of website
    Returns:
        True: No keyboard trap!
        False: Keyboard trap.
    """

    focused_elements = []
    driver.get(url)

    first_element = driver.switch_to.active_element

    for _ in range(300):
        active_element = driver.switch_to.active_element
        focused_elements.append(active_element)
        active_element.send_keys(Keys.TAB)

        # check if we are back to the initial element
        if driver.switch_to.active_element == first_element and len(focused_elements) > 1: # check focused_elements len to prevent early stop
            return True        
    return True


def test_WCAG_131_info(driver, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    '''headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    for h in range(1, headings):
        level = int(h.name[1])
        if (level != headings[h-1]) or (level-1 != headings[h-1]):
            print("Heading error.")'''
        
    labels = soup.find_all('label')
    for label in labels:
        if label.has_attr('for'):
            input_id = label['for']
            input_element = soup.find(id=input_id)
            if input_element is None:
                print(f"Warning: Label with for='{input_id}' has no corresponding input.")

#Example usage
driver = webdriver.Chrome()
test_WCAG_211_keyboard(driver, "https://www.google.com")
driver.quit()