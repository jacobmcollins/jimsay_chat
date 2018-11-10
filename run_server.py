from server.backend.JPCServer import JPCServer
from utl.jpc_parser.JPCProtocol import JPCProtocol
from flask import Flask, render_template, request, redirect
import threading
import json
app = Flask(__name__)


def run_server():
    server = JPCServer()
    server.run()


@app.route('/get_message', methods=['POST'])
def get_message():

    messageFromHTML = request.form['MessageBox']
    messageRecipient = request.form['chooseRecipient']
    messageLength = len(messageFromHTML)
    #
    # if request.method == "POST":
    #     messages = request.form['MessageBox']
    #     message = request.get(messages)
    #
    # if message:
    #     JPCServer.send_message(message)

    JPCProtocol(JPCProtocol.SEND, messageFromHTML, messageRecipient)
    """server.send_message(messageFromHTML, messageRecipient, messageLength)"""
    print(messageFromHTML)
    print(messageRecipient)

    return redirect('/index')


@app.route('/index', methods=['POST'])
def sendMessage():
    messageFromHTML = request.form['MessageBox']
    messageRecipient = request.form['chooseRecipient']
    if messageFromHTML:
        JPCServer.send_message(messageFromHTML)

    print(messageFromHTML)
    print(messageRecipient)

    return render_template('index.html')


@app.route('/index', methods=['GET'])
def index():

    return render_template('index.html')


if __name__ == '__main__':
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()
    app.run()
