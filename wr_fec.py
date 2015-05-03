#!/usr/bin/python2.7
import sys
import getopt
import copy

sys.path.append('./rs/')
from rs_code import rs_code
from gf import *
from channel import *
from fec import fec_code

def usage():
    print "wr_code -f <code> -c <config> -i <message> -b <block_len> -l <num_lost_pkt> "

    print "-f \n\t Code Scheme: [1] Reed Solomon [2] LDPC [3] LT"
    print "-i \n\t Message to encode"
    print "-l \n\t Max pkt lost"
    print "-b \n\t Size Src block to encode"
    print "-c \n\t Redundant Data Configuration"
    print "\n\tFEC Config"
    print "\n\t\t[1] 2 Pkt [src, coded]"
    print "\n\t\t[2] 3 Pkt [src, coded, coded]"
    print "\n\t\t[3] 4 Pkt [src/2, src/2, coded, coded]"
    print "\n\t\t[4] 4 Pkt [src, src, coded, coded]"
    print "\n\t\t[5] 2 Pkt [src, coded]"
    print "\n\t\t[6] 4 Pkt [src, coded, coded, coded]"
    print "\n\t\t[7] 4 Pkt [src/2, src/2, coded, coded]"

def len_arg():
    if (len(sys.argv) == 1) :
        raise RuntimeError('No arguments')
    return 0

def main(argv):

    code_sch = 0
    block_ln = 0
    fec_cfg = 0
    msg_file = ""
    decoded = 0
    failed = 0
    fec_rslt = 0
    lost_pkt = 0

    try:
        len_arg()
    except Exception:
        usage()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "hf:c:l:i:b:", ["help"])
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
            fec_cfg = int(arg, 10)
        elif opt == '-b':
            block_ln = int(arg, 10)
        elif opt == '-l':
            lost_pkt = int(arg, 10)
        elif opt == '-c':
            if (arg == 0):
                usage()
            else:
                code_sch = int(arg, 10)

    fec = fec_code(code_sch, fec_cfg, block_ln)

    msg = fec.get_data(msg_file)

    enc_msg = fec.encode(msg)

    print "ENC MSG:", enc_msg

    combi_err = pkt_lost_no_rep(lost_pkt,fec.pkt)

    channel_print(combi_err)

    for j in range(0,len(combi_err)):

        enc_msg_t = copy.copy(enc_msg)

        print "Packet Lost", combi_err[j]
        channel_lose_pkt(enc_msg_t, combi_err[j])

        dec_msg = []
        for i in range(0, len(enc_msg_t)):
            fec_rslt = fec.decode(enc_msg_t[i], dec_msg)

        fec.init()

        if (fec_rslt == fec.OK):
            print "DECODED Msg"
            print dec_msg
            print "--------------------------"
            decoded += 1

            continue
        elif (fec_rslt == fec.TRYING):
            print "FAIL to decode!!!"
            print "--------------------------"
            failed += 1
            continue

    print "Resume, Decoded: ", decoded, "Failed: ", failed

if __name__ == "__main__":
    main(sys.argv[1:])
