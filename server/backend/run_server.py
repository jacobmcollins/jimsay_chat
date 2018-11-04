import socket


class JPCServer:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 50001))

    def run(self):
        self.s.listen(1)
        running = True
        while running:
            conn, addr = self.s.accept()
            print('Client is at {}'.format(addr))
            data = conn.recv(1000000)
            print('Sending data {}'.format(data.decode()))
            conn.send(data)
            conn.close()


if __name__ == '__main__':
    server = JPCServer()
    server.run()
