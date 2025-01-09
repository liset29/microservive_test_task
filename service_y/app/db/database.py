from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service_x.config import DATABASE_URL
from service_y.app.db.models import Base

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()
# использовать const

Base.metadata.create_all(bind=engine)
