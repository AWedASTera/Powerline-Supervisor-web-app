import json
import sqlite3
import os
import datetime
from flask import Flask, jsonify, abort, request, make_response, url_for, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

dfdata = []

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

    
@app.route('/todo/api/v1.0/pillars', methods = ['GET'])
def get_pillars():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM pillars")
    pillars = c.fetchall()
    c.close()
    conn.close()
    return jsonify( { 'pillars': pillars } )

@app.route('/todo/api/v1.0/pillars/<int:pillar_id>', methods = ['GET'])
def get_pillar(pillar_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM pillars where id=?", pillar_id)
    pillars = c.fetchone()
    c.close()
    conn.close()
    if len(pillar) == 0:
        abort(404)
    return jsonify( { 'pillar': make_public_pillar(pillar[0]) } )

@app.route('/todo/api/v1.0/pillars', methods = ['POST'])
def create_pillar():
    if not request.json or not 'data' in request.json:
        abort(400)
    conn = sqlite3.connect('data.db')
    try:
        c = conn.cursor()
        c.execute("INSERT INTO pillars (data, date_time, is_stable) VALUES (?,?,?)", ( request.json['data'],  str(datetime.datetime.now()),  request.json['is_stable']))
        conn.commit()
    except sqlite3.Error as error:
        conn.rollback()
        print("Ошибка при работе с SQLite", error)
    conn.close()
    socketio.emit('update_page', namespace = '/test')
    return 201

@app.route('/todo/api/v1.0/pillars/<int:pillar_id>', methods = ['PUT'])
def update_pillar(pillar_id):
    conn = sqlite3.connect('data.db')
    if not request.json:
        abort(400)
    try:
        c = conn.cursor()
        c.execute("UPDATE pillars SET data=?, date_time=?, is_stable=? WHERE id=?", (request.json['data'],  str(datetime.datetime.now()),  bool(request.json['is_stable']), pillar_id,))
        conn.commit()
    except sqlite3.Error as error:
        conn.rollback()
        print("Ошибка при работе с SQLite", error)
    conn.close()
    socketio.emit('update_page', namespace = '/test')
    return 200
    
@app.route('/todo/api/v1.0/pillars/<int:pillar_id>', methods = ['DELETE'])
def delete_pillar(pillar_id):
    conn = sqlite3.connect('data.db')
    try:
        c = conn.cursor()
        c.execute('DELETE FROM pillars WHERE id=?', (pillar_id,))
        conn.commit()
        res = True
    except sqlite3.Error as error:
        conn.rollback()
        print("Ошибка при работе с SQLite", error)
        res = False
    conn.close()
    print(res)
    socketio.emit('update_page', namespace = '/test')
    return '200'

@socketio.on('connect', namespace = '/test')
def init_connect():
    print('Client connected')
    socketio.emit('update_page', namespace = '/test')
    

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.isfile('data.db'):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE pillars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT,
            data TEXT,
            is_stable BOOL
            )""")
        conn.commit()
        c.execute("INSERT INTO pillars (data, date_time, is_stable) VALUES (?,?,?)",  ('(0.0, 0.1)',  '2020-03-21',  True,))
        conn.commit()
        c.execute("INSERT INTO pillars (data, date_time, is_stable) VALUES (?,?,?)",  ('(0.2, 0.55)',  '2020-03-25',  True,))
        conn.commit()
        conn.close()
    socketio.run(app, debug = True, port = 80)