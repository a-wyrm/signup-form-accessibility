# Resources: https://blog.pamelafox.org/2023/07/automated-accessibility-audits-for.html
# https://playwright.dev/
# https://pamelafox.github.io/axe-playwright-python/

from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
import csv


axe = Axe()


with open('signup_urls_SMALL.csv', newline='') as csvfile:
        with sync_playwright() as playwright:
            reader = csv.DictReader(csvfile)
            for row in reader:
                browser = playwright.chromium.launch()
                page = browser.new_page()

                # Need to account for 'playwright._impl._errors.Error: Page.goto: net::ERR_EMPTY_RESPONSE' error here
                try:
                    page.goto(row['Signup'])
                    results = axe.run(page)
                    browser.close()
                except Exception as error:
                     print("Error occured: ", error)
                     continue
    
print(results.save_to_file())


# Filter results for WCAG 2.A violations
# wcag2a_violations = [violation for violation in results['violations'] if violation['impact'] == 'serious' and violation['type'] == 'wcag2a']

# # Print the WCAG 2.A violations
# if wcag2a_violations:
#     print("WCAG 2.A Violations:")
#     for violation in wcag2a_violations:
#         print(f"- {violation['id']}: {violation['message']}")
# else:
#     print("No WCAG 2.A violations found.")