from client.pi3.JPCClient import JPCClient
import random

if __name__ == '__main__':
    client = JPCClient('localhost')
    i = 0
    while i < 10:
        x = str(random.randint(0, 100000))
        print(x)
        client.send(x)
        i += 1

