import sys
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from config import username, password
import re
from bs4 import BeautifulSoup
import csv
import os, requests


class Scrapper:
    LOGIN_URL = "https://www.facebook.com"

    def __init__(self) -> None:
        chrome_options = Options()

        # disable notification pop-up
        chrome_options.add_argument("--disable-notifications")
        service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self, username, password) -> None:

        self.driver.get(self.LOGIN_URL)
        time.sleep(1)
        email_ = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div["
                                                    "1]/form/div[1]/div[1]/input")
        pass_ = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div["
                                                   "1]/form/div[1]/div[2]/div/input")
        email_.send_keys(username)
        time.sleep(1)
        pass_.send_keys(password)
        time.sleep(1)
        submitBtn = self.driver.find_element(By.XPATH,
                                             "/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div["
                                             "2]/button")
        submitBtn.click()
        time.sleep(5)

    def collect_posts_and_save(self, user_id):
        self.driver.get(f"https://www.facebook.com/{user_id}/")
        time.sleep(2)

        post_links = self.driver.find_element(By.XPATH,
                                              value='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div['
                                                    '1]/div/div/div[4]/div[2]/div/div[2]')
        text = post_links.get_attribute('outerHTML')

        soup = BeautifulSoup(text, 'html.parser')
        post_text = soup.get_text('\n')
        lines = post_text.strip().split('\n')

        # Open a CSV file for writing
        with open("posts.csv", 'w', newline='') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write each line to the CSV file
            for line in lines:
                writer.writerow(line.split(','))
        print("Successfully all the posts have been saved into a csv")

    def collect_profile_and_save(self, profile):
        url = f'https://www.facebook.com/search/top?q={profile}'
        self.driver.get(url)
        see_all_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div['
                                                  '1]/div[2]/div/div/div/div/div/div[1]/div/div/div/div/div['
                                                  '3]/a/div/div[1]'))
        )

        # Click the "See All" button
        see_all_button.click()
        time.sleep(5)

        profile_links = self.driver.find_element(By.XPATH,
                                                 value='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div['
                                                       '1]/div[1]/div[2]/div/div/div/div')
        text = profile_links.get_attribute('outerHTML')
        pattern = r'href=[\'"]?(https?://(?:www\.)?facebook\.com(?:(?!&amp;)[^\'" >])+)'

        # Find all occurrences of the pattern in the text
        urls = re.findall(pattern, text)
        urls = list(set(urls))

        # Write the list elements to the CSV file
        with open("profiles.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for element in urls:
                # Write each element as a separate row
                writer.writerow([element])
        print("Successfully all the profiles have been saved into a csv")

    def collect_images_and_save(self, user_id):
        self.driver.get(f"https://www.facebook.com/{user_id}/photos/")
        time.sleep(4)

        try:
            image_links = self.driver.find_element(By.XPATH,
                                                   value='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div['
                                                         '1]/div/div/div[4]/div[2]/div/div[1]/div/div['
                                                         '2]/div/div/div/div/div/div[2]/div/div')
            html = image_links.get_attribute('outerHTML')

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find all the img tags
            img_tags = soup.find_all('img')

            if len(img_tags) > 0:
                # Create a directory to save the images
                os.makedirs('images', exist_ok=True)

                # Iterate through the img_tags and download the images
                for i, img_tag in enumerate(img_tags):
                    src = img_tag['src']
                    src = src.strip().replace('\n', '')
                    # Download the image
                    response = requests.get(src)

                    # Save the image to the images folder
                    with open(f'images/image_{i}.jpg', 'wb') as f:
                        f.write(response.content)

                print("Images have been downloaded and saved.")
            else:
                print("This profile has no public photo or access to this profile's photo page")

        except NoSuchElementException:
            print("XPath not found.")


if __name__ == "__main__":
    scraper = Scrapper()
    # scraper.login(username, password)
    # scraper.collect_images_and_save("Ratul") #working example
    #scraper.collect_images_and_save("Sadia")  # Non-working example

    # # # Argument from command line
    func = sys.argv[1]
    arg1 = sys.argv[2]

    if func == "2":
        scraper.collect_profile_and_save(arg1)
    if func == "3":
        scraper.collect_posts_and_save(arg1)
    if func == "4":
        scraper.collect_images_and_save(arg1)
