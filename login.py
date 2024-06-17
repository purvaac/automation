import time  #  For time-related operations
import logging  #  For logging events
from selenium import webdriver  # For browser automation
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.common.keys import Keys  # For keyboard keys
from selenium.webdriver.support.ui import WebDriverWait  # For waiting for elements
from selenium.webdriver.support import expected_conditions as EC  # For defining wait conditions
from dotenv import load_dotenv  # To load environment variables from .env file
import os  # For interacting with the operating system

# Configure logging to both console and file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the file handler and set the formatter
file_handler = logging.FileHandler('automation.log')  
file_handler.setLevel(logging.INFO)  
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Define log message format
logger.addHandler(file_handler)  

# Load environment variables from .env file
load_dotenv()

# Get login creds from .env file
username = os.getenv("USERNAME")  
password = os.getenv("PASSWORD")  

if not username or not password:
    message = "USERNAME or PASSWORD environment variable is not set."
    logger.error(message)  # Log error if missing creds 
    print(message)  
    raise ValueError("Please set USERNAME and PASSWORD environment variables")  # Raise ValueError if credentials are missing

# Initialize Safari driver
message = "Initializing Safari driver..."
logger.info(message)  # Log initialization of Safari driver
print(message)  
driver = webdriver.Safari()  # Initialize Safari WebDriver

try:
    # Open Stack Overflow login page
    message = "Opening Stack Overflow login page..."
    logger.info(message)  # Log opening of Stack Overflow login page
    print(message)  
    driver.get("https://stackoverflow.com/users/login")  # Open Stack Overflow login page in browser

    # Wait for the login form to load
    wait = WebDriverWait(driver, 10)  # Initialize WebDriverWait with timeout of 10 seconds
    login_form = wait.until(EC.presence_of_element_located((By.ID, "login-form")))  # Wait until login form is present

    # Fill in the username and password fields
    message = "Logging in with username..."
    logger.info(message)  # Log filling username field
    print(message)  
    username_field = wait.until(EC.presence_of_element_located((By.ID, "email")))  # Locate username field
    username_field.send_keys(username)  # Enter username into username field

    message = "Logging in with password..."
    logger.info(message)  # Log filling password field
    print(message)  
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))  # Locate password field
    password_field.send_keys(password)  # Enter password into password field

    # Submit the login form
    password_field.send_keys(Keys.RETURN)  # Submit the login form by pressing Enter key

    # Wait for the page to load after login
    time.sleep(5)  # Wait for 5 seconds 

    # Check if login was successful
    if "stackoverflow.com/users/login" in driver.current_url:
        message = "Login failed. Please check your credentials."
        logger.error(message)  # Log login failure
        print(message)  
    else:
        message = "Login successful. Performing further actions..."
        logger.info(message)  # Log login success
        print(message)  
        

    # Keep the browser open until the user decides to close it manually
    input("Press Enter to close the browser...")

finally:
    # Close the browser only when user confirms
    driver.quit()  # Quit the browser session
    message = "Browser closed."
    logger.info(message)  # Log browser closure
    print(message) 