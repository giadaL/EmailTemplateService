from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_CONFIG
from models import db_create_all


def _db_init():
    engine = create_engine(
        DB_CONFIG.dbUri,
        echo=True
    )

    db_create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


SESSION = _db_init()
