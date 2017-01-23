import getopt
import socket
import sys

from Crypto.PublicKey import RSA
from Utils import strip, fill


def start_server(port, private_key):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port))
    server.listen(5)
    while True:
        client, _ = server.accept()

        message = int(strip(client.recv(4096)))
        new_m = private_key.sign(message, 10001)[0]
        client.send(fill(str(new_m)))

        client.close()
        sys.exit(0)


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "p:S:")

    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-p':
            port = int(arg)
        if opt == '-S':
            private_key = RSA.importKey(open(arg, 'r').read())
    start_server(port, private_key)


main()
