from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import *

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean)

    def __init__(self, username, password, disabled=False):
        self.username = username
        self.hashed_password = password
        self.disabled = disabled

    def __repr__(self):
        return f"<User('{self.username}', ID:'{self.id}')>"


engine = create_engine(
    f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{database}'
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
