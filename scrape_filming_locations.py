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

for movie in movie_data:
    movie_id = movie["source_id"]
    driver.get(f'https://www.imdb.com/title/{movie_id}/locations/')
    time.sleep(0.5)
    try:
        locations = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="sub-section-flmg_locations"] a[data-testid="item-text-with-link"]')
        print("locations: ", locations)
        movie["filming_locations"] = [loc.text.strip() for loc in locations]

    except:
        print("error")
        movie["filming_locations"] = None

    modified_movies_data.append(movie)
    

with open('movie_data.json', 'w') as f:
    json.dump(modified_movies_data, f, ensure_ascii=False, indent=4)
