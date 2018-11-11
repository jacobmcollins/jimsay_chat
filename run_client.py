from client.pi3.JPCClient import JPCClient
import random
import time

if __name__ == '__main__':
    client = JPCClient('localhost')
    start = time.time()
    for i in range(10000):
        time.sleep(1)
        now = time.time()
        if now - start >= 3:
            start = now
            print(now)
            client.send_heartbeat()
        #client.send(str(random.randint(0, 100000)))

