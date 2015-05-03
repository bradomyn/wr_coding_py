import sys
from random import seed
from random import randrange
from random import randint
import itertools

def channel_errors(msg, n_k):
    err_max = n_k
    seed()
    num_err = randint(1, err_max)
    err_pkt = []

    for i in range (0, num_err):
        err = randint(1, err_max)
        if err in err_pkt:
            continue
        err_pkt.append(err)
        msg[err] = 0x0

    return err_pkt

def channel_pkt_err(fec_msg, err_max):

    seed()

    err_loc = []

    pkt_lost = randint(0, err_max)

    for i in range(0, pkt_lost):
        pkt_miss = randint(0, pkt_lost)
        del fec_msg[pkt_miss]
        err_loc.append(pkt_miss)

    return err_loc

def pkt_lost_no_rep(x, y): # combination of Y packets taken in X
    pkt = map(str,range(0, y))

    pkt_lost = []
    lost = []

    pkt_lost_str = list(map(" ".join, itertools.permutations(pkt, x)))

    for i in range(0, len(pkt_lost_str)):
        lost.append(pkt_lost_str[i].split(' '))
        pkt_lost.append(map(int, lost[i]))

    return pkt_lost

def channel_lose_pkt(msg, lost):

    for i in range(0,len(lost)):
        for j in range(0, len(msg)):
            msg_s = msg[j]
            if (msg_s[1] == lost[i]):
                del msg[j]
                break

def channel_print(combi_err):

    print "Combination of Lost Packets", combi_err


def pkt_lost_rep(x, y):
    pkt = map(str,range(0, y))

    pkt_lost = []

    pkt_lost_str = list(map(" ".join, itertools.combinations(pkt, x)))

    for i in range(0, len(pkt_lost_str)):
        pkt_lost.append(pkt_lost_str[i].split(' '))

    return pkt_lost
