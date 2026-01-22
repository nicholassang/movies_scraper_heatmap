from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from backend.logger import get_logger

logger = get_logger(__name__)

def scrape_filming_locations():
    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_argument("--headless=new")   
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=service, options=options)

    with open('./backend/data/raw_movie_data.json', 'r') as file:
        movie_data = json.load(file)

    modified_movies_data = []

    length = len(movie_data)

    for i, movie in enumerate(movie_data):
        logger.info(f"Extracting filming locations: {i} / {length}")
        print(f"Extracting filming locations: {i} / {length}")

        movie_id = movie["source_id"]
        driver.get(f'https://www.imdb.com/title/{movie_id}/locations/')
        time.sleep(0.5)
        try:
            locations = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="sub-section-flmg_locations"] a[data-testid="item-text-with-link"]')
            movie["filming_locations"] = [loc.text.strip() for loc in locations]

        except:
            logger.error("filming_locations error")
            print("filming_locations error")
            movie["filming_locations"] = None

        modified_movies_data.append(movie)
        

    with open('./backend/data/raw_movie_data.json', 'w') as f:
        json.dump(modified_movies_data, f, ensure_ascii=False, indent=4)
