import os
from pathlib import Path

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "dev-token")
DATABASE_PATH = Path(os.environ.get("DATABASE_PATH", "data/workshop.db"))
DEFAULT_PAGE_SIZE = 20
