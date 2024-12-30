# backend/__init__.py
import dotenv
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s %(lineno)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler()
    ]
)


dotenv.load_dotenv()