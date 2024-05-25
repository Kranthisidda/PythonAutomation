import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("C://Users/krant/test_log.txt"),
        logging.StreamHandler()
    ]
)


# Function to get HTTP response code
def get_http_response_code(url):
    response = requests.get(url)
    return response.status_code, response.elapsed.total_seconds()


# Main script
try:
    # Check HTTP response code
    url = "https://atg.party"
    status_code, response_time = get_http_response_code(url)
    logging.info(f"HTTP Response Code: {status_code}")
    logging.info(f"Response Time: {response_time} seconds")
    sleep(7)
    if status_code != 200:
        raise Exception(f"Website returned status code {status_code}")

    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the website
    driver.get(url)
    start_time = time.time()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    load_time = time.time() - start_time
    logging.info(f"Page Load Time: {load_time} seconds")

    # Wait for the LOGIN button and click on it using class name
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "outer-header__loginbtn"))
    )
    login_button.click()

    # Wait for the email field and enter credentials
    email_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "email_landing"))
    )
    email_field.send_keys("wiz_saurabh@rediffmail.com")

    password_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "password_landing"))
    )
    password_field.send_keys("Pass@123")

    # Click the Sign In button to submit the form
    sign_in_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "landing-signin-btn"))
    )
    sign_in_button.click()

    # Ensure login is successful by checking for the presence of a specific element after login
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='article']"))
    )

    # Go to the article creation page
    driver.get("https://atg.party/article")

    # Fill in the title and description
    title_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "title"))
    )
    title_field.send_keys("Python Automation in Web Development")

    description_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='codex-editor codex-editor--narrow codex-editor--empty']"))

    )
    description_field.click()

    description = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='ce-paragraph cdx-block']"))
    )
    description.send_keys("selenium is a power full tool for automation")

    image_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "add-cover-image"))

    )
    image_field.click()

    cover_image_field = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "add-cover-image"))
    )
    # Adjust the path to your image
    cover_image_field.click()
    image = driver.find_element(By.ID,'cover_image')
    image.send_keys(r"C:\\Users\\krant\\Downloads\\cover_image.jpg")
    # Click on POST button
    sleep(4)

    post_button = driver.find_element(By.ID,'hpost_btn')
    post_button.click()



    sleep(10)
    # Log the URL of the new page
    new_page_url = driver.current_url
    logging.info(f"New Page URL: {new_page_url}")


finally:
    # Close the WebDriver
    driver.quit()
