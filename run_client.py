from client.pi3.JPCClient import JPCClient
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type=str, help="server ip address")
    args = parser.parse_args()
    client = JPCClient(args.ip)
    client.run()
