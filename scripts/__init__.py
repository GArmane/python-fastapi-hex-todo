import asyncio
import logging
from todolist.infra.database.seeds import run as run_seeds

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seeder():
    logger.info("Initializing seeder...")
    asyncio.run(run_seeds())
    logger.info("Seeder terminated successfully!")
