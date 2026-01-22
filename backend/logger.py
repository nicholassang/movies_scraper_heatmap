import logging
import os

log_path = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_path, exist_ok=True)

log_file = os.path.join(log_path, "app.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Helper to get module-specific loggers
def get_logger(name: str):
    return logging.getLogger(name)

# Output Logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)