from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            description TEXT,
            status TEXT
        )
    ''')
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        location = request.form['location']
        description = request.form['description']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO reports (location, description, status) VALUES (?, ?, ?)",
                     (location, description, 'Pending'))
        conn.commit()
        conn.close()

        return render_template('report.html', success=True)

    return render_template('report.html')

@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM reports").fetchall()
    conn.close()

    return render_template('view.html', reports=data)

if __name__ == '__main__':
    app.run(debug=True)