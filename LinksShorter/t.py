from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import string
import random
import re

# --- إعداد التطبيق ---
app = Flask(__name__)

# إعداد قاعدة البيانات MySQL
DATABASE_URL = "mysql+aiomysql://user:password@localhost/links_db"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- إعداد قاعدة البيانات باستخدام Async ---
engine = create_async_engine(DATABASE_URL, echo=True)
Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Link(Base):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(100), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)

# --- الحماية والتحقق من البيانات ---
def validate_url(url):
    regex = re.compile(
        r'^(https?|ftp):\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(\/.*)?$', re.IGNORECASE
    )
    return re.match(regex, url)

def validate_slug(slug):
    return re.match(r'^[a-zA-Z0-9_-]{3,20}$', slug)

async def is_slug_unique(slug):
    async with Session() as session:
        result = await session.execute(
            db.select(Link).filter_by(short_url=slug)
        )
        return result.scalar() is None

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# --- الصفحة الرئيسية ---
@app.route('/', methods=['GET', 'POST'])
async def home():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        custom_slug = request.form.get('custom_slug')

        # التحقق من الرابط الأصلي
        if not validate_url(original_url):
            return jsonify({"error": "Invalid URL format."}), 400

        # التحقق من slug المخصص
        if custom_slug:
            if not validate_slug(custom_slug):
                return jsonify({"error": "Invalid slug format."}), 400
            if not await is_slug_unique(custom_slug):
                return jsonify({"error": "Slug already exists. Try another one."}), 400
            short_url = custom_slug
        else:
            # توليد رابط عشوائي إذا لم يتم تحديد slug
            short_url = generate_short_url()

        # حفظ الرابط في قاعدة البيانات
        async with Session() as session:
            new_link = Link(original_url=original_url, short_url=short_url)
            session.add(new_link)
            await session.commit()

        return jsonify({"short_url": f'http://localhost:5000/{short_url}'})

    return render_template('index.html')

# --- إعادة التوجيه ---
@app.route('/<short_url>')
async def redirect_to_url(short_url):
    async with Session() as session:
        result = await session.execute(
            db.select(Link).filter_by(short_url=short_url)
        )
        link = result.scalar()

        if link:
            link.clicks += 1
            await session.commit()
            return redirect(link.original_url)
        else:
            return jsonify({"error": "URL not found."}), 404

# --- تشغيل التطبيق ---
if __name__ == '__main__':
    import os

    # إعداد الهيكل الأساسي للمشروع
    if not os.path.exists('LinksShorter/static'):
        os.makedirs('LinksShorter/static')
    if not os.path.exists('LinksShorter/templates'):
        os.makedirs('LinksShorter/templates')

    with open('LinksShorter/templates/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Link Shortener</title>
</head>
<body>
    <h1>Link Shortener</h1>
    <form method="POST">
        <label for="original_url">Enter URL:</label>
        <input type="url" id="original_url" name="original_url" required />
        <br />
        <label for="custom_slug">Custom Slug (optional):</label>
        <input type="text" id="custom_slug" name="custom_slug" />
        <br />
        <button type="submit">Shorten</button>
    </form>
</body>
</html>
''')

    app.run(debug=True)
