from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time, random
import json
from movie_details_utils import *
from advanced_search_utils import *

selected_country = "US"

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

no_pages = 5 # expands movie list by 50 (Initial no_pages = 0: 50 movies)

# Load into website 
driver.get(get_website())
time.sleep(0.5)

# Filter to movies only
filter_movies_only(wait)
time.sleep(0.5)

# Click on country filter
click_country_filter(driver, wait)

# Filter by country (specific)
filter_country(wait, selected_country)
time.sleep(0.5)

# Actual Search
actual_search(wait)
time.sleep(0.5)

# Click more
for _ in range(no_pages):
    click_more_movies(wait, driver)
    time.sleep(0.5)



# Wait until all movies link in the page are found (50)
movie_links = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ipc-title-link-wrapper"))
)

# Extract href and text for all movies
movies = []
for a in movie_links:
    href = a.get_attribute("href")          
    title = a.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
    movies.append((title, href))

# Print all movie titles and links
for title, link in movies:
    print(title, link)

time.sleep(0.5)

# =========================================================
# === Scrape movie details from movies in the page (50) ===
# =========================================================

all_movies_data = []
no_movies_to_get = 100 #editable

for _ in range(no_movies_to_get):
    movie_link = movies[_][1]
    driver.get(movie_link)

    time.sleep(0.5)

    movie_data = {}

    # Source_Id
    get_movie_source_id(movie_data, movie_link)

    # Title
    get_movie_title(movie_data, driver)

    # Year
    get_movie_year(movie_data, driver)

    # Rating
    get_movie_rating(movie_data, driver)

    # Budget
    get_movie_budget(movie_data, driver)

    # Gross
    get_movie_gross(movie_data, driver)

    # ROI
    get_movie_ROI(movie_data, driver)

    # Genres
    get_movie_genres(movie_data, driver)

    # Production Country
    get_movie_prod_cntry(movie_data, selected_country)


    # Click on img overlay inside Movie's Details
    img_overlay = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[class="ipc-lockup-overlay ipc-focusable ipc-focusable--constrained"]')
        )
    )
    img_overlay.click()

    # poster_url
    get_movie_poster_url(movie_data, driver)


    all_movies_data.append(movie_data)
    time.sleep(0.5)


time.sleep(1)

with open("movie_data.json", "w", encoding="utf-8") as f:
    json.dump(all_movies_data, f, ensure_ascii=False, indent=4)


