from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_CONFIG
from src.models import db_create_all

_engine = create_engine(DB_CONFIG.dbUri,
                        echo=True)


def _db_init():
    db_create_all(_engine)


def _session_create():
    Session = sessionmaker(bind=_engine)
    return Session()


SESSION = _session_create
