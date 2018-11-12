from server.backend.JPCServer import JPCServer
from utl.jpc_parser.JPCProtocol import JPCProtocol
from flask import Flask, render_template, request, redirect
import threading
import csv
import string
app = Flask(__name__)


def run_server(server):
    server.run()
    server.send_message("lindsay", "abc")


def shift_string(my_string, shift):
    alph_string = string.ascii_letters # string of both uppercase/lowercase letters
    return ''.join([chr(ord(c)+shift) if c in alph_string else c for c in my_string])


@app.route('/get_message', methods=['POST'])
def get_message():
    messageFromHTML = request.form['MessageBox']
    messageRecipient = request.form['chooseRecipient']
    messageLength = len(messageFromHTML)
    messages = []
    messageLog = open("messageLog.txt", "a")
    messageLog.write("To " + messageRecipient + ": " + messageFromHTML + "\n")

    #JPCProtocol(JPCProtocol.SEND, messageFromHTML, messageRecipient)
    """server.send_message(messageFromHTML, messageRecipient, messageLength)"""
    server.send_message(messageFromHTML, messageRecipient)

    print(messageFromHTML)
    print(messageRecipient)

    messagesFile = open("messageLog.txt", "r")
    for message in messagesFile:
            messages.append(message)

    messages.reverse()

    return render_template('index.html', messages=messages[0:10], firstMessage="To " + messageRecipient + ": " + messageFromHTML + "\n")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    server = JPCServer()
    threading.Thread(target=run_server, args=[server]).start()
    app.run()
