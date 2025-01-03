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

# إنشاء الجلسة المتزامنة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """دالة لإنشاء الجداول في قاعدة البيانات"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    try:
        # استدعاء دالة إنشاء الجداول
        create_tables()
        print("تم إنشاء الجداول بنجاح.")
    except Exception as e:
        print(f"حدث خطأ: {e}")
