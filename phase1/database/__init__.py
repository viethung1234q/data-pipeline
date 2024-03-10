from config import mysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to MySQL
engine = create_engine(f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['host']}:{mysql['port']}/{mysql['database_name']}", echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()