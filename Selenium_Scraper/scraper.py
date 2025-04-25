# LinkedIn Profile Scraper using Selenium
# This script logs into LinkedIn with credentials from .env file and scrapes profiles based on search parameters

import os
import time
import csv
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# LinkedIn credentials and search parameters
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
SEARCH_QUERY = os.getenv('SEARCH_QUERY')
SEARCH_LOCATION = os.getenv('SEARCH_LOCATION')
MAX_PROFILES = int(os.getenv('MAX_PROFILES', 50))
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'False').lower() == 'true'
SCROLL_PAUSE_TIME = float(os.getenv('SCROLL_PAUSE_TIME', 2))
SAVE_TO_CSV = os.getenv('SAVE_TO_CSV', 'True').lower() == 'true'
OUTPUT_FILENAME = os.getenv('OUTPUT_FILENAME', 'linkedin_profiles')

# Set up ChromeDriver
driver = None

def init_driver():
    global driver
    if driver is None:
        st.write("Initializing Chrome browser...")
        # Set up Chrome options
        chrome_options = Options()
        # Always show the browser window
        chrome_options.add_argument("--start-maximized")  # Start with maximized window
        chrome_options.add_argument("--disable-notifications")  # Disable notifications
        chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Set up ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        st.write("Chrome browser initialized successfully!")
    return driver

def close_driver():
    global driver
    if driver is not None:
        driver.quit()
        driver = None
        st.write("Browser closed successfully!")

# Add a random delay to mimic human behavior
def random_delay(min_seconds=1, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Function to login to LinkedIn
def login_to_linkedin():
    st.write("Logging into LinkedIn...")
    driver = init_driver()
    driver.get("https://www.linkedin.com/login")
    random_delay()

    try:
        # Enter email
        st.write("Entering email...")
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.clear()
        email_field.send_keys(LINKEDIN_EMAIL)
        random_delay(0.5, 1.5)

        # Enter password
        st.write("Entering password...")
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(LINKEDIN_PASSWORD)
        random_delay(0.5, 1.5)

        # Click login button
        st.write("Clicking login button...")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Wait for login to complete
        st.write("Waiting for login to complete...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
        st.success("Login successful!")
        random_delay()

    except Exception as e:
        st.error(f"Login failed: {e}")
        close_driver()
        exit(1)

# Function to search for profiles
def search_profiles():
    st.write(f"Searching for '{SEARCH_QUERY}' in '{SEARCH_LOCATION}'...")
    driver = init_driver()
    # Navigate to LinkedIn search page
    driver.get("https://www.linkedin.com/search/results/people/")
    random_delay()

    try:
        # Click on search bar
        st.write("Entering search query...")
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]"))
        )
        search_bar.clear()
        search_bar.send_keys(SEARCH_QUERY)
        search_bar.send_keys(Keys.RETURN)
        random_delay()

        # Add location filter if provided
        if SEARCH_LOCATION:
            try:
                st.write("Applying location filter...")
                # Click on 'Locations' filter dropdown
                location_filter = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Locations') or contains(@aria-label, 'Locations')]"))
                )
                location_filter.click()
                random_delay()

                # Enter location
                location_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Add a location')]"))
                )
                location_input.clear()
                location_input.send_keys(SEARCH_LOCATION)
                random_delay(1, 2)

                # Wait for location suggestions and click the first one
                location_suggestion = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'basic-typeahead')]//span[contains(@class, 'entity-result__title')]"))
                )
                location_suggestion.click()
                random_delay()

                # Click "Apply" button
                apply_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Apply') or contains(@aria-label, 'Apply')]")
                apply_button.click()
                random_delay()

            except Exception as e:
                st.warning(f"Could not apply location filter: {e}")

        st.success("Search filters applied successfully!")

    except Exception as e:
        st.error(f"Search failed: {e}")
        close_driver()
        exit(1)

# Function to extract profile data
def extract_profile_data(profile_url):
    driver = init_driver()
    driver.get(profile_url)
    random_delay(2, 4)

    try:
        profile_data = {
            "URL": profile_url,
            "Name": "",
            "Title": "",
            "Location": "",
            "About": "",
            "Experience": [],
            "Education": [],
            "Skills": []
        }

        # Extract name
        try:
            profile_data["Name"] = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]"))
            ).text
        except (TimeoutException, NoSuchElementException):
            profile_data["Name"] = "Not Found"

        # Extract title
        try:
            profile_data["Title"] = driver.find_element(By.XPATH, "//div[contains(@class, 'text-body-medium')]").text
        except NoSuchElementException:
            profile_data["Title"] = "Not Found"

        # Extract location
        try:
            profile_data["Location"] = driver.find_element(By.XPATH, "//span[contains(@class, 'text-body-small') and contains(@class, 'inline')]").text
        except NoSuchElementException:
            profile_data["Location"] = "Not Found"

        # Extract About section
        try:
            about_section = driver.find_element(By.XPATH, "//section[.//div[contains(text(), 'About')]]//div[contains(@class, 'display-flex')]")
            profile_data["About"] = about_section.text
        except NoSuchElementException:
            profile_data["About"] = "Not Found"

        # Extract Experience
        try:
            experience_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//section[.//div[contains(text(), 'Experience')]]"))
            )
            experience_items = experience_section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")

            for item in experience_items:
                try:
                    role = item.find_element(By.XPATH, ".//span[contains(@class, 'mr1') and contains(@class, 't-bold')]").text
                    company = item.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal')]").text
                    date_range = item.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and contains(@class, 't-black--light')]").text
                    profile_data["Experience"].append(f"{role} at {company} ({date_range})")
                except NoSuchElementException:
                    continue
        except (TimeoutException, NoSuchElementException):
            pass

        # Extract Education
        try:
            education_section = driver.find_element(By.XPATH, "//section[.//div[contains(text(), 'Education')]]")
            education_items = education_section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")

            for item in education_items:
                try:
                    school = item.find_element(By.XPATH, ".//span[contains(@class, 't-bold')]").text
                    degree = item.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal')]").text
                    profile_data["Education"].append(f"{school} - {degree}")
                except NoSuchElementException:
                    continue
        except NoSuchElementException:
            pass

        # Extract Skills
        try:
            # Click "Skills" to view all skills
            skills_button = driver.find_element(By.XPATH, "//section[.//div[contains(text(), 'Skills')]]//a[contains(text(), 'Show all')]")
            skills_button.click()
            random_delay()

            # Extract skills from the modal that appears
            skills_modal = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'artdeco-modal__content')]"))
            )
            skill_items = skills_modal.find_elements(By.XPATH, ".//div[contains(@class, 'display-flex align-items-center')]//span[contains(@class, 't-bold')]")

            for skill in skill_items:
                profile_data["Skills"].append(skill.text)

            # Close the skills modal
            close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'artdeco-modal__dismiss')]")
            close_button.click()
            random_delay()

        except (TimeoutException, NoSuchElementException):
            try:
                # If "Show all" is not available, try to get skills directly from the profile
                skills_section = driver.find_element(By.XPATH, "//section[.//div[contains(text(), 'Skills')]]")
                skill_items = skills_section.find_elements(By.XPATH, ".//span[contains(@class, 't-bold')]")

                for skill in skill_items:
                    profile_data["Skills"].append(skill.text)
            except NoSuchElementException:
                pass

        return profile_data

    except Exception as e:
        print(f"Error extracting profile data: {e}")
        return None

# Function to scrape profiles from search results
def scrape_profiles():
    print("Starting to scrape profiles...")
    driver = init_driver()
    profile_urls = []
    profiles_data = []
    page_num = 1

    while len(profile_urls) < MAX_PROFILES:
        try:
            print(f"Scanning page {page_num} of search results...")

            # Wait for profile cards to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'reusable-search__entity-result-list')]"))
            )
            random_delay()

            # Scroll down to load all profiles on the page
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Get profile links from current page
            profile_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'entity-result__title-text')]/a")

            for element in profile_elements:
                profile_url = element.get_attribute('href')
                if profile_url and '/in/' in profile_url:
                    # Clean the URL to remove tracking parameters
                    clean_url = profile_url.split('?')[0]
                    if clean_url not in profile_urls:
                        profile_urls.append(clean_url)

                    if len(profile_urls) >= MAX_PROFILES:
                        break

            if len(profile_urls) >= MAX_PROFILES:
                break

            # Try to go to the next page
            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next')]")
                if next_button.is_enabled():
                    next_button.click()
                    page_num += 1
                    random_delay(2, 4)
                else:
                    print("No more pages to scan.")
                    break
            except NoSuchElementException:
                print("No more pages to scan.")
                break

        except Exception as e:
            print(f"Error scanning page {page_num}: {e}")
            break

    # Extract data from each profile
    print(f"Found {len(profile_urls)} profiles. Starting data extraction...")
    for i, url in enumerate(profile_urls):
        print(f"Extracting profile {i+1}/{len(profile_urls)}: {url}")
        profile_data = extract_profile_data(url)
        if profile_data:
            profiles_data.append(profile_data)
        random_delay(3, 6)  # Add delay between profile visits to avoid getting blocked

    return profiles_data

# Function to save profiles data to CSV
def save_to_csv(profiles_data):
    if not profiles_data:
        print("No profile data to save.")
        return

    filename = f"{OUTPUT_FILENAME}.csv"

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Create flat structure for CSV
            fieldnames = [
                'URL', 'Name', 'Title', 'Location', 'About',
                'Experience', 'Education', 'Skills'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for profile in profiles_data:
                # Convert lists to strings for CSV format
                flat_profile = profile.copy()
                flat_profile['Experience'] = '|'.join(profile['Experience'])
                flat_profile['Education'] = '|'.join(profile['Education'])
                flat_profile['Skills'] = '|'.join(profile['Skills'])

                writer.writerow(flat_profile)

        print(f"Successfully saved {len(profiles_data)} profiles to {filename}")

    except Exception as e:
        print(f"Error saving to CSV: {e}")