from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine("sqlite:///todooo.db")

Base = declarative_base()



