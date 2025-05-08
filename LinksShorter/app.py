from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from LinksShorter.config import SessionLocal
from LinksShorter.models import Links, User
from LinksShorter.functions import generate_short_link
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

app_index = Blueprint('app_index', __name__, template_folder='templates')

@app_index.route("/", methods=["GET"])
def index():
  return render_template("index.html")

@app_index.route("/cshorter", methods=["POST"])
def create_shorter():
  data = request.get_json()
  original_link = data.get("original_link")
  
  session = SessionLocal()
  try:
    db_link = session.execute(
      select(Links).filter(Links.original_url == original_link)
    ).scalars().first()
    
    if db_link:
      return jsonify({"shorter": db_link.short_url}), 200
    
    chshort = generate_short_link()
    db_link = Links(
      original_url=original_link,
      short_url=chshort,
      clicks=0
    )
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return jsonify({"shorter": chshort}), 202
  finally:
    session.close()

@app_index.route('/not-found')
def not_found():
  return render_template("not-found.html")

@app_index.route('/<path:short_u>')
def redirect_to_link(short_u):
  session = SessionLocal()
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

@app_index.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  
  # POST method
  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')
  confirm_password = request.form.get('confirm-password')

  if not name or not email or not password or not confirm_password:
    flash('Please fill out all fields.', 'error')
    return render_template('register.html', name=name, email=email)

  if password != confirm_password:
    flash('Passwords do not match.', 'error')
    return render_template('register.html', name=name, email=email)

  session = SessionLocal()
  try:
    existing_user = session.execute(
      select(User).filter(User.email == email)
    ).scalars().first()

    if existing_user:
      flash('Email already registered.', 'error')
      return render_template('register.html', name=name, email=email)

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    session.add(new_user)
    session.commit()
    flash('Registration successful. Please log in.', 'success')
    return redirect(url_for('app_index.index'))
  finally:
    session.close()
