import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
driver_path = '/path/to/chromedriver'
url = input("Enter the URL to scrape: ")

# Define CSS selectors in a dictionary to adapt to different websites
selectors = {
    'contact_button': 'a.btn.btn-primary.btn-block',  # CSS selector for contact buttons
    'call_button': 'div.phonemasked-button',          # CSS selector for the call button
    'phone_number': 'a.phonemasked-phone.text-center.visible-xs.visible-sm',  # CSS selector for phone number
    'close_button': 'button.close.modal-close'        # CSS selector for modal close button
}

# Setup Chrome WebDriver options
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# Visit the URL
driver.get(url)

# List to hold extracted phone numbers
phone_numbers = []

try:
    # Find and iterate over contact buttons
    contact_buttons = driver.find_elements(By.CSS_SELECTOR, selectors['contact_button'])
    for index, button in enumerate(contact_buttons):
        try:
            # Re-find contact buttons to avoid stale elements
            contact_buttons = driver.find_elements(By.CSS_SELECTOR, selectors['contact_button'])
            driver.execute_script("arguments[0].scrollIntoView();", contact_buttons[index])
            driver.execute_script("arguments[0].click();", contact_buttons[index])

            # Wait for and click the call button
            call_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['call_button']))
            )
            driver.execute_script("arguments[0].click();", call_button)

            # Retrieve the phone number
            phone_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selectors['phone_number']))
            )
            phone_number = phone_element.text.strip()
            if phone_number:
                phone_numbers.append(phone_number)
                print(f'Phone number found: {phone_number}')

            # Close the modal
            close_button = driver.find_element(By.CSS_SELECTOR, selectors['close_button'])
            driver.execute_script("arguments[0].click();", close_button)

        except Exception as e:
            print(f"Error at index {index}: {e}")

finally:
    driver.quit()

# Write the phone numbers to a CSV file
if phone_numbers:
    with open('phone_numbers.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for phone_number in phone_numbers:
            writer.writerow([phone_number])
            print(f'Phone number {phone_number} written to CSV.')
else:
    print('No phone numbers found.')
