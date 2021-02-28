import threading
from flask import Flask
from waitress import serve

from scanner import test


app = Flask(__name__)
scanner = threading.Thread(target=test)


@app.route('/')
def index():
    return f'Job alive: {scanner.is_alive()}'


if __name__ == '__main__':
    scanner.start()
    serve(app)
