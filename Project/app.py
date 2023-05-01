import os
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# путь к корневой директории проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# относительный путь к файлу базы данных
DATABASE = os.path.join(PROJECT_ROOT, 'projects.db')


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
