from backend.ETL.scrapers.scrape_imdb import scrape_imdb
from backend.ETL.scrapers.scrape_filming_locations import scrape_filming_locations
from backend.logger import get_logger

logger = get_logger(__name__)

def extract(no_movies_to_get_para = 5):
    logger.info("Extract Running...")
    print("Extract Running...")
    print()
    scrape_imdb(no_movies_to_get_para) # para => (no_movies_to_get_para:int = 1, selected_country:string = 'US')
    scrape_filming_locations()
