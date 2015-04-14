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