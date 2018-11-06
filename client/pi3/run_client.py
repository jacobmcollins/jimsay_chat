from client.pi3.JPCClient import JPCClient


if __name__ == '__main__':
    # client = JPCClient('131.252.208.23')
    client = JPCClient('localhost')
    client.send('abcdefgh')
    data = client.receive()
    print(data.decode())
    print('received {} bytes'.format(len(data)))
    client.close()
