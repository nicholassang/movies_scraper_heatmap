from backend.ETL.extract import extract
from backend.ETL.transform import transform
from backend.ETL.load import load
from backend.logger import get_logger

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


