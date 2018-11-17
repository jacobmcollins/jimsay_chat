from client.pi3.JPCClient import JPCClient

if __name__ == '__main__':
    client = JPCClient('192.168.0.21')
    client.run()
