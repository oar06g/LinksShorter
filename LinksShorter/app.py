from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from LinksShorter.config import SessionLocal
from LinksShorter.models import Links
from LinksShorter.functions import generate_short_link
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

app_index = Blueprint('app_index', __name__, template_folder='templates')

@app_index.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app_index.route("/cshorter", methods=["POST"])
def create_shorter():
    data = request.get_json()
    original_link = data.get("original_link")
    
    # فتح الجلسة المتزامنة بشكل صحيح
    session = SessionLocal()  # تم تعديل هذا السطر لاستخدام SessionLocal() بدلاً من db_session()
    try:
        db_link = session.execute(
            select(Links).filter(Links.original_url == original_link)
        ).scalars().first()
        
        if db_link:
            return jsonify({"shorter": db_link.short_url}), 200
        
        # إذا لم يتم العثور على الرابط
        chshort = generate_short_link()
        db_link = Links(
            original_url=original_link,
            short_url=chshort,
            clicks=0
        )
        session.add(db_link)
        session.commit()  # تنفيذ عملية الحفظ بشكل متزامن
        session.refresh(db_link)
        return jsonify({"shorter": chshort}), 202
    finally:
        session.close()  # التأكد من إغلاق الجلسة بعد انتهاء العملية

@app_index.route('/not-found')
def not_found():
    return "<h1>Not found</h1>"

@app_index.route('/<path:short_u>')  # يسمح بأي نص بعد /
def redirect_to_link(short_u):
  session = SessionLocal()  # تم تعديل هذا السطر لاستخدام SessionLocal() بدلاً من db_session()
  try:
      db_link = session.execute(
          select(Links).filter(Links.short_url == short_u)
      ).scalars().first()
      
      if db_link:
        db_link.clicks += 1
        session.commit()
        return redirect(db_link.original_url)
      
      return redirect(url_for("app_index.not_found"))
  finally:
      session.close()