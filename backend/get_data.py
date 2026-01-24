from ETL.extract import extract
from ETL.transform import transform
from ETL.load import load
from logger import get_logger

logger = get_logger(__name__)

def run_etl():
    logger.info("ETL job started")

    try:
        extract(100)
        transform()
        load()
        logger.info("ETL job completed successfully")

    except Exception as e:
        logger.exception("ETL job failed")


