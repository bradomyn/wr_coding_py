import sys
sys.path.append('./rs/')

from rs_code import rs_code

class fec_cfg:
    op = [[] for l in range(0, 4) ]

    def __init__(self):
        fec_cfg.op[0] = {'pkt': 2, 'n': 256, 'k' : 128}
        fec_cfg.op[1] = {'pkt': 3, 'n': 252, 'k' : 84}
        fec_cfg.op[2] = {'pkt': 4, 'n': 256, 'k' : 128}
        fec_cfg.op[3] = {'pkt': 4, 'n': 256, 'k' : 64}


class fec_code:
    pkt = 4
    TRYING = 1
    FAIL = 2
    OK = 3
    ID_IDX = 1
    SYM_IDX = 3
    dec_msg = []
    cfg = fec_cfg()

    def __init__(self, code_id, fec_cfg, block_ln):

        cfg =  fec_code.cfg.op[code_id - 1]

        self.ratio = cfg['n'] / cfg['k']
        self.alpha = cfg['pkt'] / self.ratio # number of packets with src symbols
        self.beta =  cfg['pkt'] - self.ratio # number of packts with enc symbols
        self.code_id = code_id
        fec_code.pkt = cfg['pkt']
        self.block_symbol = cfg['k']
        self.pkt_ln = block_ln / self.alpha
        self.code_iter = self.pkt_ln / self.block_symbol
        self.block_ln = block_ln

        fec_code.dec_msg = [0] * self.block_ln
        self.pkt_id = 0
        self.recv_msg = 0

        if code_id == 1:
            self.code = rs_code(cfg['n'], cfg['k'])

    def get_data(self, msg_file):

        f = open(msg_file,'r')
        msg_input = f.read(self.block_ln)
        msg_int_byte = [0] * len(msg_input)
        for i in range(0, len(msg_input)):
            msg_int_byte[i] = ord(msg_input[i])

        return msg_int_byte

    def encode(self, msg):
        fec_msg = [[] for l in range(0, self.pkt) ]

        # FEC header
        for i in range(0, self.pkt):
            fec_msg[i].append(self.code_id)
            fec_msg[i].append(i)
            b_symbol = self.block_symbol * i
            fec_msg[i].append(b_symbol)

        # FEC payload
        slice_pkt = self.pkt_ln / self.block_symbol

        for i in range(0, self.code_iter):
            slice = i * self.block_symbol
            enc_msg = self.code.encode(msg[slice : slice + self.block_symbol])
            #systematic original msg
            fec_msg[i % slice_pkt].apend(enc_msg[: self.block_symbol])

            #encode msg
            if (self.beta - self.alfa > 1): # one src pkt is encoded into one pkt
                fec_msg[(i % slice_pkt) + self.ratio].apend(enc_msg[self.block_symbol + 1 :])
            else:                           # one src pkt is encoded in more than one pkt
                for j in range (0, self.beta):
                    enc_slice = (j + 1) * (self.block_symbol + 1)
                    fec_msg[(i % slice_pkt) + j].apend(enc_msg[ enc_slice : enc_slice + self.block_symbol ])
        return fec_msg

    def decode(self, msg):

        #msg_id  = msg[self.ID_IDX]
        #fec_symbols = msg[self.SYM_IDX][:]

        if (msg_id == 0 | msg_id == 1):
            fec_code.dec_msg[msg_id * 512 : (msg_id + 1) * 512] = fec_symbols
            self.recv_msg += 250

            if (self.recv_msg == 500):
                return fec_code.OK
        elif (msg_id == 2 | msg_id == 3):
            print "ehllo"
            #self.code.decode(fec_symbols, lost_pkt)

        return 1
