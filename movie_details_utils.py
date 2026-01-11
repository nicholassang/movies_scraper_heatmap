from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import re

movie_details_selectors = {
    "title": (By.CSS_SELECTOR, '[data-testid="hero__primary-text"]'),
    "year": (By.CSS_SELECTOR, 'ul.ipc-inline-list li a[href*="releaseinfo"]'),
    "rating": (By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"] span:first-child'),
    "budget": (By.CSS_SELECTOR, 'li[data-testid="title-boxoffice-budget"] span.ipc-metadata-list-item__list-content-item'),
    "gross": (By.CSS_SELECTOR, 'li[data-testid="title-boxoffice-cumulativeworldwidegross"] span.ipc-metadata-list-item__list-content-item'),
    "genres": (By.CSS_SELECTOR, 'div.ipc-chip-list__scroller span.ipc-chip__text'),
    "poster_url" : (By.CSS_SELECTOR, "div[data-testid='media-viewer'] img")
}

# Source_Id
def get_movie_source_id(movie_data, movie_link):
    path = urlparse(movie_link).path
    imdb_id = path.split('/')[2]
    movie_data["source_id"] = imdb_id

# Title
def get_movie_title(movie_data, driver):
    try:
        movie_data["title"] = driver.find_element(*movie_details_selectors["title"]).text.strip()
    except:
        movie_data["title"] = None

# Year
def get_movie_year(movie_data, driver):
    try:
        movie_data["year"] = driver.find_element(*movie_details_selectors["year"]).text.strip()
    except:
        movie_data["year"] = None

# Rating
def get_movie_rating(movie_data, driver):
    try:
        movie_data["rating"] = driver.find_element(*movie_details_selectors["rating"]).text.strip()
    except:
        movie_data["rating"] = None

# Budget
def get_movie_budget(movie_data, driver):
    try:
        budget_text = driver.find_element(*movie_details_selectors["budget"]).text.strip()
        
        match = re.search(r'\$([\d,]+)', budget_text)
        if match:
            movie_data["budget"] = int(match.group(1).replace(',', ''))
        else:
            movie_data["budget"] = None
    except:
        movie_data["budget"] = None

# Gross
def get_movie_gross(movie_data, driver):
    try:
        gross_text = driver.find_element(*movie_details_selectors["gross"]).text.strip()

        match = re.search(r'\$([\d,]+)', gross_text)
        if match:
            movie_data["gross"] = int(match.group(1).replace(',', ''))
        else:
            movie_data["gross"] = None
    except:
        movie_data["gross"] = None

# ROI
def get_movie_ROI(movie_data, driver):
    if movie_data.get("gross") is not None and movie_data.get("budget") is not None and movie_data["budget"] != 0:
        movie_data["ROI"] = round(((movie_data["gross"] - movie_data["budget"]) / movie_data["budget"]) * 100, 1)
    else:
        movie_data["ROI"] = None

# Genres
def get_movie_genres(movie_data, driver):
    try:
        genre_elements = driver.find_elements(*movie_details_selectors["genres"])
        movie_data["genres"] = [g.text.strip() for g in genre_elements]
    except:
        movie_data["genres"] = []

# Production Country
def get_movie_prod_cntry(movie_data, selected_country):
    try:
        movie_data["production_country"] = selected_country
    except:
        movie_data["genres"] = None

# Poster URL
def get_movie_poster_url(movie_data, driver):
    try:
        movie_data["poster_url"] = driver.find_element(*movie_details_selectors["poster_url"]).get_attribute("src")
    except:
        movie_data["poster_url"] = None