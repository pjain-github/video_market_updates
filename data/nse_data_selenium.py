# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# import os

# # Set download directory (Modify as per your system)
# download_dir = os.path.join(os.getcwd(), "elements")   # Adjust this for Windows

# # Set Chrome options for automatic download
# chrome_options = webdriver.ChromeOptions()
# prefs = {"download.default_directory": download_dir}
# chrome_options.add_experimental_option("prefs", prefs)

# # Initialize WebDriver
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.nseindia.com/reports-indices-historical-index-data")

# # Wait for the dropdown to be interactable
# wait = WebDriverWait(driver, 10)
# dropdown = wait.until(EC.element_to_be_clickable((By.ID, "hpReportIndexTypeSearchInput")))

# # Click the dropdown to open it
# dropdown.click()
# time.sleep(2)  # Allow options to load
# select = Select(dropdown)
# select.select_by_visible_text("NIFTY 50")

# # Delay to confirm selection
# time.sleep(2)

# # Correct XPath for the 1M link (using contains text and targeting <a> tag)
# one_month_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '1M')]")))
# one_month_link.click()

# # Wait for Download CSV button and click
# download_button = wait.until(EC.element_to_be_clickable((By.ID, "CFanncEquity-download")))
# download_button.click()

# # Wait for the file to be downloaded
# time.sleep(10)  # Adjust as needed based on download speed

# print("CSV file downloaded in:", download_dir)

# # Close the browser
# driver.quit()

