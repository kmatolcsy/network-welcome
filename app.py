import threading
from flask import Flask, url_for, redirect
from waitress import serve

from scanner import test


app = Flask(__name__)
event = threading.Event()
scanner = threading.Thread(target=test, args=(event, ))


@app.route('/')
def index():
    return f'Job alive: {scanner.is_alive()} Event set: {event.is_set()}'


@app.route('/toogle')
def toogle():
    event.clear() if event.is_set() else event.set()

    return redirect(url_for('index'))


if __name__ == '__main__':
    scanner.start()
    serve(app)
