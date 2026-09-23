import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [AlertX2-Android] [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
app_logger = logging.getLogger("alertx2_app")
