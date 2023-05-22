import sqlite3
import os
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Alex/Desktop/Python/work/Project/projects.db'  # Путь к базе данных SQLite
app.config['SECRET_KEY'] = '@4p*Ygb9T9'  # Секретный ключ для сессии Flask

db = SQLAlchemy(app)
bcrypt = Bcrypt()

# путь к корневой директории проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# относительный путь к файлу базы данных
DATABASE = os.path.join(PROJECT_ROOT, 'projects.db')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Пользователь с таким именем уже существует'

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return 'Пользователь с таким email уже существует'

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Поиск пользователя в базе данных
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Успешная авторизация
            session['user_id'] = user.id
            return redirect('/')

        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    session['logged_in'] = False
    return redirect('/')


@app.route('/protected')
def protected():
    if 'user_id' in session:
        return 'This is a protected page'
    return redirect('/login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM projects WHERE title LIKE ?', ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
