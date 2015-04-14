#!/usr/bin/python2.7
import sys
import getopt
from rs_code import rs_code
from gf import *
sys.path.append('../')
from channel import *

def usage():
    print "rs -k K -n N -i message"
    print "-k K \n \t Number of source symbol"
    print "-n N \n \t Number of encoded symbols"
    print "-i message \n \t source symbols file "

def len_arg():
    if (len(sys.argv) == 1) :
        raise RuntimeError('No arguments')
    return 0

def main(argv):

    rs = rs_code()

    try:
        len_arg()
    except Exception:
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hi:k:n:", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-i':
            msg_file = arg
        elif opt == '-k':
            rs.k = int(arg, 10)
        elif opt == '-n':
            rs.n = int(arg, 10)

    message = open(msg_file,'r')
    msg_input = message.read().split(', ')
    msg_in = [0] * len(msg_input)

    for i in range (0, len(msg_input)):
        msg_in[i] = int(msg_input[i], 16)

    rs.print_poly("SRC_MSG", msg_in)

# Encode
    msg = rs.encode(msg_in)
    rs.print_poly("ENC_MSG", msg)

# Transmission the packets
    err = channel_errors(msg, rs.n_k)

    print "Number of Errors in Tx", len(err)
    rs.print_poly("TX_MSG", msg)

# Decoding

    rs.decode(msg, err)

    rs.print_poly("DEC_MSG", msg)

if __name__ == "__main__":
    main(sys.argv[1:])