from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

advanced_search_selector = {
    "website": "https://www.imdb.com/search/title/",
    "movie_btn": (By.CSS_SELECTOR, '[data-testid="test-chip-id-movie"]'),
    "country_btn": (By.CSS_SELECTOR, '[data-testid="accordion-item-countryAccordion"]'),
    "scroll_country_btn": 'arguments[0].scrollIntoView({block: "center"});',
    "country_search": (By.CSS_SELECTOR, '[data-testid="autosuggest-input-test-id-countries"]'),
    "search_btn": (By.CSS_SELECTOR, '[data-testid="adv-search-get-results"]'),
    "click_more_btn": (By.CSS_SELECTOR, '[class="ipc-see-more__text"]'),
    "scroll_to_page_bottom": "window.scrollTo(0, document.body.scrollHeight);",
    "get_document_height": "return document.body.scrollHeight",
}

# Load into website
def get_website():
    return advanced_search_selector["website"]

# Filter to movies only
def filter_movies_only(wait, driver):
    movie_btn = wait.until(
        EC.presence_of_element_located(advanced_search_selector["movie_btn"])
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", movie_btn)
    movie_btn = wait.until(
        EC.element_to_be_clickable(advanced_search_selector["movie_btn"])
    )
    movie_btn.click()

# Click on country filter
def click_country_filter(driver, wait):
    country_btn = wait.until(
        EC.element_to_be_clickable(
            advanced_search_selector["country_btn"]
        )
    )
    driver.execute_script(advanced_search_selector["scroll_country_btn"], country_btn)
    time.sleep(0.5)
    country_btn.click()

# Filter by country (specific)
def filter_country(wait, selected_country):
    country_search = wait.until(
        EC.element_to_be_clickable(
            advanced_search_selector["country_search"]
        )
    )
    country_search.send_keys(selected_country)

# Actual Search
def actual_search(wait):
    search_btn = wait.until(
        EC.element_to_be_clickable(
            advanced_search_selector["search_btn"]
        )
    )
    search_btn.click()

# Click to get more movies
def click_more_movies(wait, driver):
    click_more_btn = wait.until(
        EC.element_to_be_clickable(
            advanced_search_selector["click_more_btn"]
        )
    )
    driver.execute_script(advanced_search_selector["scroll_to_page_bottom"])
    time.sleep(1)

    click_more_btn.click()

    last_height = driver.execute_script(advanced_search_selector["get_document_height"])
    
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script(advanced_search_selector["get_document_height"]) > last_height
    )
