from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from LinksShorter.config import engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String(500), nullable=False)
    short_url = Column(String(100), unique=True, nullable=False)
    clicks = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
  try:
    create_tables()
  except Exception as e:
    print(f"حدث خطأ: {e}")
