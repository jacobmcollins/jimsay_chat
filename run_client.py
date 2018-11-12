from client.pi3.JPCClient import JPCClient
import random
import time

if __name__ == '__main__':
    client = JPCClient('192.168.0.14')
    start = time.time()
    for i in range(5):
        time.sleep(2)
        client.send_heartbeat()
    time.sleep(6)
    client.send_heartbeat()

