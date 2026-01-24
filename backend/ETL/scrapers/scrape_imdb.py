from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from .movie_details_utils import *
from .advanced_search_utils import *
from logger import get_logger
from pathlib import Path

logger = get_logger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
raw_file_path = DATA_DIR / "raw_movie_data.json"

def scrape_imdb(no_movies_to_get_para, selected_country = "US"):

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

    service = Service(ChromeDriverManager().install())

    # service=service removed to sync with docker
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    no_pages = no_movies_to_get_para // 50 # expands movie list by 50 (Initial no_pages = 0: 50 movies)

    if no_pages < 0:
        logger.error("Negative numbers not allowed")
        print("Negative numbers not allowed")
        return

    # ==========================================================================================
    # === Set up the indicated capacity (no_pages) movies in the page for Selenium to scrape ===
    # ==========================================================================================

    # Load into website 
    driver.get(get_website())
    time.sleep(0.5)

    # Filter to movies only
    filter_movies_only(wait, driver)
    time.sleep(0.5)

    """ # Click on country filter
    click_country_filter(driver, wait)

    # Filter by country (specific)
    filter_country(wait, selected_country)
    time.sleep(0.5) """ # Commented out country filter (not needed)

    # Actual Search
    actual_search(wait)
    time.sleep(0.5)

    # Click to get more movies
    for _ in range(no_pages):
        click_more_movies(wait, driver)
        time.sleep(0.5)

    # ==================================================
    # === Scrap movies IMDB movie IDs and hyperlinks ===
    # ==================================================

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

    # LOGGING: Print all movie titles and links for retrieve
    for title, link in movies[:no_movies_to_get_para]:
        logger.info(f"{title} {link}")
        print(title, link)

    print()
    time.sleep(0.5)

    # ==============================================================================
    # === EXTRACT & TRANSFORM: Scrape movie details from movies in the page (50) ===
    # ==============================================================================

    all_movies_data = []
    no_movies_to_get = no_movies_to_get_para #editable

    try:
        for _ in range(no_movies_to_get):
            movie_link = movies[_][1]
            driver.get(movie_link)
            time.sleep(0.5)

            movie_data = {}

            logger.info(f"Processing movie {_ + 1} / {no_movies_to_get}: {movies[_][0]}")
            print(f"Processing movie {_ + 1} / {no_movies_to_get}: {movies[_][0]}")

            # Source_Id
            get_movie_source_id(movie_data, movie_link)

            # Title
            get_movie_title(movie_data, driver)

            # Year
            get_movie_year(movie_data, driver)

            # Country
            get_movie_country(movie_data, driver)

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

        with open(raw_file_path, "w", encoding="utf-8") as f:
            json.dump(all_movies_data, f, ensure_ascii=False, indent=4)

        print()

    except:
        logger.info("Collected: ", len(all_movies_data))
        print("Collected: ", len(all_movies_data))

        with open(raw_file_path, "w", encoding="utf-8") as f:
            json.dump(all_movies_data, f, ensure_ascii=False, indent=4)

        print()