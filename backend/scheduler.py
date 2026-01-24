import logging
from apscheduler.schedulers.background import BackgroundScheduler
from get_data import run_etl
from datetime import datetime

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler():
    logger.info("Starting scheduler")

    scheduler.add_job(
        run_etl,
        trigger="interval",
        hours=6,
        id="etl_job",
        replace_existing=True,
        max_instances=1,
        # next_run_time=datetime.now() # Scheduler runs immediately 
    )

    scheduler.start()

def shutdown_scheduler():
    logger.info("Shutting down scheduler")
    scheduler.shutdown(wait=False)