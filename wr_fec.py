#!/usr/bin/python2.7
import sys
import getopt

sys.path.append('./rs/')
from rs_code import rs_code
from gf import *
from channel import *
from fec import fec_code

def usage():
    print "wr_code -f <code> -c <config> -i <message> -l <block_len>"

    print "-f \n\t Code Scheme: [1] Reed Solomon [2] LDPC [3] LT"
    print "-i \n\t Message to encode"
    print "-c \n\t Redundant Data Configuration"
    print "\n\tFEC Config"
    print "\n\t\t[1] 2 Pkt [src, coded]"
    print "\n\t\t[2] 3 Pkt [src, coded, coded]"
    print "\n\t\t[3] 4 Pkt [src, coded, coded, coded]"
    print "\n\t\t[4] 4 Pkt [src/2, src/2, coded, coded]"

def len_arg():
    if (len(sys.argv) == 1) :
        raise RuntimeError('No arguments')
    return 0

def main(argv):

    code_sch = 0
    block_ln = 0
    fec_cfg = 0
    msg_file = ""

    try:
        len_arg()
    except Exception:
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hi:c:l:i:", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-i':
            msg_file = arg
        elif opt == '-f':
            code_sch = arg
        elif opt == '-l':
            block_ln = arg
        elif opt == '-c':
            if (arg == 0):
                usage()
            else:
                fec_cfg = arg

    fec = fec_code(code_sch, fec_cfg, block_ln)

    msg = fec.get_data(msg_file)

    enc_msg = fec.encode(msg)

    err = channel_pkt_err(enc_msg, fec.pkt)

    print "Tx Packet - ", len(err), "lost packet"

    for i in range(0, len(enc_msg)):
        fec_rslt = fec.decode(enc_msg[i])

        if (fec_rslt == fec.OK):
            print "Decoded Msg"
            exit(0)
        elif (fec_rslt == fec.TRYING):
            continue
        elif (fec_rslt == fec.FAIL):
            print "Fail to decode!!!"
            exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
