import time, re, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

def setup_driver():
    """Sets up the Chrome WebDriver with extension and options."""
    service = Service()
    options = webdriver.ChromeOptions()
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

import signup_vocab

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
            #print(f"aria-label: {aria_label_text}")

            text_in_element = _.text.replace(" ", "").lower()
            #print(f"element text: {text_in_element}")

            if (aria_label_text not in text_in_element):
                return False
            
    return True

def test_247_visible(driver, url):
    """
    Tests that focus is visible.

    Args:
        driver: Chrome driver.
        url: URL of website
    Returns:
        True: No 2.4.7 violation!
        False: 2.4.7 violation.

    """
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
            return False
        else:
            #print(f"Element {element} does have a focus.")
            continue
    
    return True


def enter_email(field):
    for regex in signup_vocab.usernameVocabs:
        if regex.search(str(field)) or regex.search(str(field.get('type'))) or regex.search(str(field.get('id'))):
            return field
def enter_pw(field):
    for regex in signup_vocab.passwordVocabs:
        if regex.search(str(field)) or regex.search(str(field.get('type'))) or regex.search(str(field.get('id'))):
            return field

def enter_pw_field(driver, input_field):
    try: 
        selenium_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//input[@type='{input_field.get('type')}']"))
        )
        selenium_select.send_keys("a")

        time.sleep(10)
        return True
    
    except Exception as e:
        try:
            selenium_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, input_field.get('id')))
            )
            return True #success
        except Exception as e2:
            print(f"Failed to click button with class and text '{input_field}': {e2}")
            return False    
def enter_email_field(driver, input_field):
    try: 
        selenium_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//input[@type='{input_field.get('type')}']"))
        )
        selenium_select.send_keys("a@gmail.com")
        return True
    
    except Exception as e:
        try:
            selenium_select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, input_field.get('id')))
            )
            return True #success
        except Exception as e2:
            print(f"Failed to click button with class and text '{input_field}': {e2}")
            return False


def enter_info(driver, username_email, password_field):

    username_has_required = ('required' in username_email.attrs)
    pw_has_required = ('required' in password_field.attrs)

    # We want to get the password field... not the email field
    if password_field and not pw_has_required and username_has_required:
        enter_email_field(driver, username_email)
        return False
    elif username_email and not username_has_required and pw_has_required:
        enter_pw_field(driver, password_field)
        return False
    elif not username_has_required and not pw_has_required:
        return False
    else:
        return True

def find_errors(driver):

    soup = BeautifulSoup(driver.page_source, 'lxml')
    potential_error_divs = []

    # Find divs based on ID
    id_matches = soup.find_all(['div', 'p' 'ul'], id=re.compile(r'.*(error|err|alert).*', re.IGNORECASE))
    potential_error_divs.extend(id_matches)

    # Find divs based on class.
    class_matches = soup.find_all(['div', 'p', 'ul'], class_=re.compile(r'.*(error|err|alert).*', re.IGNORECASE))
    potential_error_divs.extend(class_matches)

    # Find divs based on role.
    role_matches = soup.find_all(['div', 'p', 'ul'], role_=re.compile(r'.*(alert).*', re.IGNORECASE))
    potential_error_divs.extend(role_matches)

    #remove duplicates
    unique_error_divs = list(dict.fromkeys(potential_error_divs))

    if unique_error_divs != []:
        print(f'Potential error divs: {unique_error_divs}')
        return True
    
    return False

def test_331_errorid(driver, url):
    """
    Tests that focus is visible.

    Args:
        driver: Chrome driver.
        url: URL of website
    Returns:
        True: No 2.4.7 violation!
        False: 2.4.7 violation.

    """

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    buttons = soup.find_all(['button'])
    potential_buttons = soup.find_all(['div', 'span'], {"class": re.compile(r'btn'), "role": "button"})

    form_fields = soup.find_all(['input'])
    hidden_tag = soup.find("input", {'type': 'password'}) # fields may be hidden
    if hidden_tag:
        form_fields.append(hidden_tag)

    # divs and spans can sometimes be buttons (inaccessible)
    for add_buttons in potential_buttons:
        buttons.append(add_buttons)


    div_signup_button = soup.find("input", {'type': 'submit'})

    if div_signup_button:
        buttons.append(div_signup_button)
    
    username_email = None
    password_field = None
    
    # Get pw and username field, if they exist
    time.sleep(random.randint(1, 6)) 
    for field in form_fields:
        if_username_email = enter_email(field)
        if_password = enter_pw(field)

        if if_username_email is not None:
            username_email = if_username_email
        if if_password is not None:
            password_field = if_password
        
    for _ in buttons:
        button_text = _.text.strip()
        button_val = _.get('value')
        for pattern in signup_vocab.registerVocabs: 
            if pattern.search(button_text) or (button_val and pattern.search(button_val)):

                print(f"Clickable button: {_}")

                try: 
                    selenium_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[normalize-space()='{button_text}']"))
                    )

                    check_if_required_field_exists = enter_info(driver, username_email, password_field)
                    if (check_if_required_field_exists == True):
                        return True
                    
                    selenium_button.click()
                    
                    found_errors = find_errors(driver)
                    return found_errors
                
                except Exception as e:
                    try:
                        classes = _.get('class')
                        if button_val:
                            selenium_button = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(@value, '{button_val}')]"))
                                )
                            check_if_required_field_exists = enter_info(driver, username_email, password_field)
                            if (check_if_required_field_exists == True):
                                return True
                            selenium_button.click()
                            print(f"Clicked button with value: '{button_val}'")
                            time.sleep(10)

                            found_errors = find_errors(driver)
                            return found_errors
                        
                        elif classes:
                            for class_name in classes:
                                selenium_button = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(@class, '{class_name}')]"))
                                )
                                check_if_required_field_exists = enter_info(driver, username_email, password_field)
                                if (check_if_required_field_exists == True):
                                    return True
                                selenium_button.click()
                                time.sleep(10)

                                found_errors = find_errors(driver)
                                return found_errors
                    except Exception as e2:
                        print(f"Failed to click button with class and text '{button_text}': {e2}")
                        return "Error"

    return "Possible error: may be regex issue"

driver = setup_driver()

#passes_131 = test_WCAG_131_info(driver, "https://burtsgh.com/my-account/")
# passes_131 and
# https://www.athleticsmania.com/?gotoManageAccount
# https://affcoups.com/register/
passes_247 = test_331_errorid(driver, "https://www.zopiclonepill.com/my-account/?action=register")
print(passes_247)
driver.quit()