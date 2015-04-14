#!/usr/bin/python2.7
import sys
import getopt

sys.path.append('./rs/')
from rs_code import rs_code
from gf import *
from channel import *
from fec import fec_code

def usage():
    print "wr_code -i config"

def len_arg():
    if (len(sys.argv) == 1) :
        raise RuntimeError('No arguments')
    return 0

def main(argv):

    fec = fec_code(1)

    try:
        len_arg()
    except Exception:
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hi:", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-i':
            msg_file = arg

    msg = fec.get_data(msg_file)

    enc_msg = fec.encode(msg)

    print enc_msg[0]
    print enc_msg[1]
    print enc_msg[2]
    print enc_msg[3]


    #for i in range(0, len(msg_input)):
    #   msg[i] = int(msg_input[i],16)


if __name__ == "__main__":
    main(sys.argv[1:])
