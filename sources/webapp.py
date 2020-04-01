import sqlite3
import os
import sys
import json
import random
import logging
from functools import wraps
from flask import Flask, request, Response, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    user = get_user(username)
    return user and username == user.get('name') and password == user.get('pass')

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth:
            app.logger.info('[' + auth.username + '] ' + request.url)
            if not check_auth(auth.username, auth.password):
                return authenticate()
        else:
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    stuff = do_query('SELECT * FROM prices ORDER BY day DESC, fuel ASC', result_set_name='fuels')
    rows = stuff['fuels']
    info = []
    item = {}
    for idx, row in enumerate(rows):
        if idx and idx % 3 == 0:
            info.append(item)
            item = {}
        item['Datum'] = row['day']
        item[row['fuel']] = '{:.3f}'.format(row['price'])
    info.append(item)
    return render_template('fuels.html', fuels=info)

@app.route('/vars/')
def show_server_vars():
    info = []
    for key in sorted(request.environ):
        info.append((key, request.environ[key]))
    return render_template('vars.html', info=info)

@app.route('/greeting/', methods=['GET', 'POST'])
def greeting():
    if request.method == 'POST':
        return render_template('greeting_post.html', name=request.form['name'])
    else:
        return render_template('greeting_get.html')

@app.route('/secret/')
@requires_auth
def secret():
    return render_template('secret.html')

def get_user(name):
    return {'name': 'at', 'pass': 'geheim'}

def get_row_as_dict(row, curs):
    obj = {}
    for idx, col in enumerate(curs.description):
        obj[col[0]] = row[idx]
    return obj

def do_query(query, bindings=None, result_set_name='result set'):
    """
    Returns a dict containing a single key with
    a list of dicts as values, each dict containing
    database row data.
    """
    db = get_db()
    if bindings:
        curs = db.execute(query, bindings)
    else:
        curs = db.execute(query)
    result_set = []
    for row in curs:
        result_set.append(get_row_as_dict(row, curs))
    
    return {result_set_name: result_set}

def fetch(table, where=None, order_by=None):
    query = "SELECT * FROM " + table
    if where:
        query += " WHERE " + where
    if order_by:
        query += " ORDER BY " + order_by
    
    return do_query(query, result_set_name=table)

def connect_db():
    rv = sqlite3.connect(os.path.join(app.root_path, 'fuelprices.db'))
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

def make_json(obj):
    """
    Returns a response object with headers correctly set
    for a json text, made from a list or dict.
    """
    text = json.dumps(obj)
    resp = make_response(text)
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Content-Length'] = len(text)
    return resp

def make_plain_text(text):
    """
    Returns a response object with headers correctly set
    for a plain text
    """
    resp = make_response(text)
    resp.headers['Content-Type'] = 'text/plain'
    resp.headers['Content-Length'] = len(text)
    return resp
