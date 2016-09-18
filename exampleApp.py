import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)

app = Flask(__name__)
app.config.from_object(__name__)

# this skeleton code is from Flask tutorial
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'courseDatabase.db'),
    SECRET_KEY="secretkey"
))
app.config.from_envvar('PICKER_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('courseDatabase.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Initialized the database.'

#my stuff

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select courseNumber, courseName, courseBit from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/input')
def input_entries():
    db = get_db()
    cur = db.execute('select courseNumber, courseName, courseBit from entries order by id desc')
    entries = cur.fetchall()
    return render_template('input_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (courseNumber, courseName, courseBit) values (?, ?, ?)',
                 [request.form['courseNumber'], request.form['courseName'], request.form['courseBit']])
    db.commit()
    flash('You added a class!')
    return redirect(url_for('show_entries'))

@app.route('/filter')
def filter():
    return render_template('filter.html')

@app.route('/show-filtered', methods=['POST'])
def show_filtered_entries():
    db = get_db()
    cur = db.execute('select courseNumber, courseName, courseBit from entries where courseBit = %s order by id desc' % request.form['filterBit'])
    entries = cur.fetchall()
    return render_template('show_filtered_entries.html', entries=entries)
