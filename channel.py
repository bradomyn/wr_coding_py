import sys
from random import seed
from random import randrange

def channel_errors(msg, n_k):
    err_max = n_k /4
    seed(10)
    num_err = randrange(0, err_max, 3)
    #num_err = randint(0, err_max)
    err_pkt = []

    for i in range (0, num_err):
        err = randrange(0, num_err, 3)
        if err in err_pkt:
            continue
        err_pkt.append(err)
        msg[err] = 0x0

    return err_pkt

def channel_pkt_err(fec_msg, err_max):

    seed(10)

    err_loc = []

    pkt_lost = randrange(1, err_max, 3)

    for i in range(0, pkt_lost):
        pkt_miss = randrange(0, pkt_lost, 100)
        del fec_msg[pkt_miss]
        err_loc.append(pkt_miss)

    return err_loc