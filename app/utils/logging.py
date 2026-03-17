from pathlib import Path
import logging

log_dir = Path.home() / ".philospher_service"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(),  # also print logs to terminal
    ],
)

logger = logging.getLogger(__name__)
logger.info(f"Logger initialized. Log file: {log_file}")
