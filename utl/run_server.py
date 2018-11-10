from server.backend.JPCServer import JPCServer
from flask import Flask, render_template, request, redirect
import threading
app = Flask(__name__)


def run_server():
    server = JPCServer()
    server.run()


@app.route('/get_message', methods=['POST'])
def get_message():

    messageFromHTML = request.form['MessageBox']
    messageRecipient = request.form['chooseRecipient']
    #
    # if request.method == "POST":
    #     messages = request.form['MessageBox']
    #     message = request.get(messages)
    #
    # if message:
    #     JPCServer.send_message(message)
    print(messageFromHTML)
    print(messageRecipient)

    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        messages = request.form['MessageBox']
        message = request.get(messages)

    if message:
        JPCServer.send_message(message)

    return render_template('index.html')


if __name__ == '__main__':
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()
    app.run()
