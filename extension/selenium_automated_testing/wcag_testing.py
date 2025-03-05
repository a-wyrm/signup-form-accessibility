import time, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

""" def test_WCAG_211_keyboard(driver, url):
    Checks for a keyboard trap on a website.

    Args:
        driver: Chrome driver.
        url: URL of website
    Returns:
        True: No keyboard trap!
        False: Keyboard trap.

    focused_elements = []
    driver.get(url)

    first_element = driver.switch_to.active_element

    for _ in range(300):
        active_element = driver.switch_to.active_element
        focused_elements.append(active_element)
        active_element.send_keys(Keys.TAB)

        # check if we are back to the initial element
        if driver.switch_to.active_element == first_element and len(focused_elements) > 1: # check focused_elements len to prevent early stop
            return False        
    return True """

""" def test_WCAG_131_info(driver, url):

    Tests that information, structure, and relationships conveyed through presentation can be programmatically determined or are available in text.

    Args:
        driver: Chrome driver.
        url: URL of website
    Returns:
        True: No 1.3.1 violation!
        False: 1.3.1 violation.

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
            if input_element is None and label.text == "":
                print(f"Warning: Label with for='{input_id}' has no corresponding input.")
                return False

    return True """


def test_253(driver, url):
    """
    Tests that aria label matches text of element.

    Args:
        driver: Chrome driver.
        url: URL of website
    Returns:
        True: No 2.5.3 violation!
        False: 2.5.3 violation.

    """
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    inherits = soup.find_all(['tr', 'thread', 'tbody', 'tfoot', 'table', 'ol', 'ul', 'div', 'dl'])

    for _ in inherits:
        if _.has_attr('aria-label'):

            aria_label_text = _.get('aria-label').replace(" ", "").lower()
            print(f"aria-label: {aria_label_text}")

            text_in_element = _.text.replace(" ", "").lower()
            print(f"element text: {text_in_element}")

            if (aria_label_text not in text_in_element):
                return False
            
    return True



def test_247_visible(driver, url):

    driver.get(url)
    focusable_elements = driver.find_elements(By.XPATH, "//*[self::a or self::button or self::input or self::textarea or self::select][@href or @tabindex='0' or @type='button' or @type='submit' or @type='reset' or @type='text' or @type='password' or @type='checkbox' or @type='radio' or @type='email' or @type='number' or @type='tel']")
    #print(focusable_elements)
    num_of_unfocusable_elements = 0
    for element in focusable_elements:


        # Simulate tabbing to the element
        element.send_keys(webdriver.Keys.TAB)
        time.sleep(.5)

        element_class = ""

        if element.tag_name == 'a':
            parent_li = element.find_element(By.XPATH, "./..") # get parent
            element_class = parent_li.get_attribute("class")
        elif element.tag_name == 'li':
            element_class = element.get_attribute("class")

        #print(element_class)

        # Check for visible focus indicators (e.g., outline, border, background change)
        focus_style = element.value_of_css_property("outline")
        border_style = element.value_of_css_property("border")
        background_color = element.value_of_css_property("background-color")
    

        if focus_style == "none" and border_style == "none" and background_color == "rgba(0, 0, 0, 0)" and element_class.find("focus") != -1: #If no outline, border, or background color change.
            num_of_unfocusable_elements+=1
            #print(f"Element {element} doesn't have a focus.")
        else:
            #print(f"Element {element} does have a focus.")
            continue


driver = webdriver.Chrome()

#passes_131 = test_WCAG_131_info(driver, "https://burtsgh.com/my-account/")
# passes_131 and
passes_247 = test_253(driver, "https://45books.com/account/register")

driver.quit()