

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
import os
from LinksShorter.config import SessionLocal, engine
from models import Links
import asyncio

app = Flask(__name__)

# إعدادات قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # تعيين قيمة الرابط في ملف .env
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# تهيئة SQLAlchemy
db = SQLAlchemy(app)

# مسار لإنشاء رابط جديد
@app.route('/links', methods=['POST'])
async def create_link():
    data = request.get_json()
    original_url = data.get('original_url')
    short_url = data.get('short_url')

    if not original_url or not short_url:
        return jsonify({"msg": "Both original_url and short_url are required!"}), 400

    new_link = Links(original_url=original_url, short_url=short_url)
    
    # إضافة الرابط إلى قاعدة البيانات بطريقة غير متزامنة
    async with SessionLocal() as session:
        session.add(new_link)
        await session.commit()

    return jsonify({"msg": "Link created successfully!"}), 201

# مسار لجلب كل الروابط
@app.route('/links', methods=['GET'])
async def get_links():
    async with SessionLocal() as session:
        result = await session.execute(select(Links))
        links = result.scalars().all()
        return jsonify(links=[{'id': link.id, 'original_url': link.original_url, 'short_url': link.short_url, 'clicks': link.clicks} for link in links]), 200

# دالة لإنشاء الجداول إذا لم تكن موجودة
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.before_first_request
def before_first_request():
    asyncio.run(create_tables())

if __name__ == "__main__":
    app.run(debug=True)
