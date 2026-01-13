from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import json

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

with open('movie_data.json', 'r') as file:
    movie_data = json.load(file)

modified_movies_data = []

location = movie_data[0]["country"]
search_location = location.replace(" ", "+")

print(search_location)

driver.get(f'https://www.google.com/maps/{movie_data[0]["country"]}/')

time.sleep(10)
