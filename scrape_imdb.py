from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time, random

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

driver.get("https://www.imdb.com/search/title/")

time.sleep(2)

# Filter to movies only
movie_btn = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="test-chip-id-movie"]')
    )
)
movie_btn.click()

time.sleep(1)

# Click on country filter
country_btn = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="accordion-item-countryAccordion"]')
    )
)
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", country_btn)
time.sleep(0.5)
country_btn.click()

time.sleep(1)

# Filter by country (specific)
country_search = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="autosuggest-input-test-id-countries"]')
    )
)
country_search.send_keys("US")

time.sleep(1)

# Actual Search
search_btn = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-testid="adv-search-get-results"]')
    )
)
search_btn.click()

time.sleep(2)


# Find all movie titles
titles = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[class="ipc-title__text"]'))
)

# Wait until at least one movie link is present
movie_links = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ipc-title-link-wrapper"))
)

# Extract href and text for all movies
movies = []
for a in movie_links:
    href = a.get_attribute("href")          # full link
    title = a.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
    movies.append((title, href))

# Print all movie titles and links
for title, link in movies:
    print(title, link)

time.sleep(2)

# Go to the first Movie Link
first_link = movies[0][1]
driver.get(first_link)

time.sleep(2)

movie_details_selectors = {
    "title": (By.CSS_SELECTOR, '[data-testid="hero__primary-text"]'),
    "rating": (By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"] span:first-child'),
    "genres": (By.CSS_SELECTOR, 'div.ipc-chip-list__scroller span.ipc-chip__text')
}

movie_data = {}

# Title
try:
    movie_data["title"] = driver.find_element(*movie_details_selectors["title"]).text.strip()
except:
    movie_data["title"] = None

# Rating
try:
    movie_data["rating"] = driver.find_element(*movie_details_selectors["rating"]).text.strip()
except:
    movie_data["rating"] = None

# Genres
try:
    genre_elements = driver.find_elements(*movie_details_selectors["genres"])
    movie_data["genres"] = [g.text.strip() for g in genre_elements]
except:
    movie_data["genres"] = []


print(movie_data)


# Click on img overlay inside Movie's Details
img_overlay = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[class="ipc-lockup-overlay ipc-focusable ipc-focusable--constrained"]')
    )
)
img_overlay.click()

time.sleep(2)

# Exit img overlay, return to Movie's Details
driver.back()

time.sleep(2)

#return nack to search page
driver.back()

time.sleep(5)


