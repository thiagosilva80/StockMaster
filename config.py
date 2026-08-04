import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "stockmaster-chave-local")

    # SQLite simplifica a publicação no Render: não exige servidor MySQL,
    # usuário, senha, host ou porta.
    DATABASE_PATH = Path(
        os.environ.get("DATABASE_PATH", str(BASE_DIR / "stockmaster.db"))
    )
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
