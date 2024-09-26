# Resources: https://blog.pamelafox.org/2023/07/automated-accessibility-audits-for.html
# https://playwright.dev/
# https://pamelafox.github.io/axe-playwright-python/

from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
import csv
from pathlib import Path

cwd = Path.cwd()
axe = Axe()


with open('signup_urls_fix.csv', newline='') as csvfile:
        with sync_playwright() as playwright:
            reader = csv.DictReader(csvfile)
            for row in reader:
                browser = playwright.chromium.launch()
                page = browser.new_page()

                # Need to account for 'playwright._impl._errors.Error: Page.goto: net::ERR_EMPTY_RESPONSE' error here
                try:
                    page.goto(row['Signup'])
                    results = axe.run(page)
                    results.save_to_file(cwd/'JSON/', row['Website']+'.json')
                    browser.close()
                except Exception as error:
                    with open('invalid.csv', 'a', newline='') as invalid_file:
                        writer = csv.writer(invalid_file)
                        writer.writerow([row['Website'], str(error)])
                    continue
    


# Filter results for WCAG 2.A violations
# wcag2a_violations = [violation for violation in results['violations'] if violation['impact'] == 'serious' and violation['type'] == 'wcag2a']

# # Print the WCAG 2.A violations
# if wcag2a_violations:
#     print("WCAG 2.A Violations:")
#     for violation in wcag2a_violations:
#         print(f"- {violation['id']}: {violation['message']}")
# else:
#     print("No WCAG 2.A violations found.")