from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main.python.ApplicationProperties import ApplicationProperties

from src.main.python.models.Profile import Profile
from src.main.python.models.Restriction import Restriction
from src.main.python.models.Follow_model import Follow
from src.main.python.models.ShoppingList import ShoppingList
from src.main.python.models.Ingredient import Ingredient

props = ApplicationProperties()

DATABASE_URL = props.database_url
POOL_SIZE = props.database_pool_size

engine = create_engine(
    DATABASE_URL,
    pool_size=POOL_SIZE,
    echo=True,
    connect_args={"connect_timeout": 10}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Profile.__table__.create(bind=engine, checkfirst=True)
Restriction.__table__.create(bind=engine, checkfirst=True)
Follow.__table__.create(bind=engine, checkfirst=True)
ShoppingList.__table__.create(bind=engine, checkfirst=True)
Ingredient.__table__.create(bind=engine, checkfirst=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
