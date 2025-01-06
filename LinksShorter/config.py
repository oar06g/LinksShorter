from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

class Config:
  def __init__(self):
    load_dotenv()
    self.username = os.getenv("USERNAME")
    self.password = os.getenv("PASSWORD")
    self.host = os.getenv("HOST")
    self.database = os.getenv("DB_NAME")
    self.port = os.getenv("PORT")
    self.database_url = self._create_database_url()
    self.engine = self._create_engine()
    self.session = self._create_session()

  def _create_database_url(self):
    return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

  def _create_engine(self):
    return create_engine(self.database_url, echo=True)

  def _create_session(self):
    return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

config = Config()
SessionLocal = config.session
engine = config.engine

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
