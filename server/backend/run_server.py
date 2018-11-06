from server.backend.JPCServer import JPCServer
from flask import Flask, render_template
import threading
app = Flask(__name__)


def run_server():
    server = JPCServer()
    server.run()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()
    app.run()
