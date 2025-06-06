from flask import Flask, render_template, request, redirect 
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def homepage():
    return render_template('home.html')
    
@app.route('/write', methods=['GET', 'POST'])
def write_entry():
    if request.method == 'POST':
        content = request.form['content']
        conn = sqlite3.connect('journal.db')
        c = conn.cursor()
        c.execute('INSERT INTO entries (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return redirect('/read')
    return render_template('write.html')
    
@app.route('/read')
def read_entries():
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()
    c.execute('SELECT * FROM entries')
    entries = c.fetchall()
    conn.close()
    return render_template('read.html', entries=entries)
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)