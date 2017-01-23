import getopt
import socket

import sys

from Crypto.PublicKey import RSA
from Crypto.Util import number
from Utils import fill, strip


def start_client(host, port, public_key, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    found = False
    while not found:
        r_blind = number.getPrime(100)
        if public_key.n % r_blind:
            found = True
    blinded = public_key.blind(message, r_blind)

    client.send(fill(str(blinded)))

    new_m = int(strip(client.recv(4096)))
    print public_key.unblind(new_m, r_blind)


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "o:p:K:M:")

    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-o':
            host = arg
        if opt == '-p':
            port = int(arg)
        if opt == '-K':
            public_key = RSA.importKey(open(arg, 'r').read())
        if opt == '-M':
            message = int(arg)

    start_client(host, port, public_key, message)


main()
