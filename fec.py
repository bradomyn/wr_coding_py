import sys
import itertools
import copy
sys.path.append('./rs/')

from rs_code import rs_code

class fec_cfg:
    op = [[] for l in range(0, 6) ]

    def __init__(self):
        fec_cfg.op[0] = {'pkt': 2, 'n': 256, 'k' : 128}
        fec_cfg.op[1] = {'pkt': 3, 'n': 252, 'k' : 84}
        fec_cfg.op[2] = {'pkt': 4, 'n': 256, 'k' : 128}
        fec_cfg.op[3] = {'pkt': 4, 'n': 256, 'k' : 64}
        fec_cfg.op[4] = {'pkt': 2, 'n': 16,  'k' : 8}
        fec_cfg.op[5] = {'pkt': 4, 'n': 16,  'k' : 8}


class fec_code:
    pkt = 4
    TRYING = 1
    FAIL = 2
    OK = 3
    ID_IDX = 1
    SYM_IDX = 3
    IDX_IDX = 2
    dec_msg = []
    recv_msg = []
    cfg = fec_cfg()


    def __init__(self, code_id, fec_cfg, block_ln):

        cfg =  fec_code.cfg.op[fec_cfg - 1]

        self.ratio = cfg['n'] / cfg['k']
        fec_code.pkt = cfg['pkt']
        self.pkt_ln = block_ln * self.ratio / fec_code.pkt
        self.alpha = cfg['pkt'] / self.ratio # number of packets with src symbols
        self.beta =  (cfg['pkt'] - self.alpha) / self.alpha # number of packets with enc symbols
        self.code_id = code_id
        self.block_symbol = cfg['k']

        self.code_iter = block_ln / self.block_symbol
        self.block_ln = block_ln

        fec_code.dec_msg = [0] * self.block_ln
        fec_code.recv_msg = [0] * self.alpha
        self.pkt_id = 0

        if code_id == 1:
            self.code = rs_code(cfg['n'], cfg['k'])

    def init(self):
        self.pkt_id = 0
        fec_code.recv_msg = [0] * self.alpha

    def get_data(self, msg_file):

        f = open(msg_file,'r')
        msg_input = f.read().split(' ')
        msg_int_byte = [0] * len(msg_input)

        for i in range(0, len(msg_input)):
            msg_int_byte[i] = int(msg_input[i], 16)
            #msg_int_byte[i] = ord(msg_input[i])

        return msg_int_byte

    def encode(self, msg):
        fec_msg = [[] for l in range(0, self.pkt) ]

        # FEC header
        for i in range(0, self.pkt):
            fec_msg[i].append(self.code_id)
            fec_msg[i].append(i)
            b_symbol = self.pkt_ln * i
            fec_msg[i].append(b_symbol)

        # FEC payload
        slice_pkt = (self.pkt_ln / self.block_symbol)

        for i in range(0, self.code_iter):
            slice = i * self.block_symbol
            enc_msg = self.code.encode(msg[slice : slice + self.block_symbol])
            #systematic original msg
            index = i / slice_pkt
            fec_msg[index].append(enc_msg[: self.block_symbol])

            for j in range (0, self.beta):
                    fec_msg[index + self.alpha + j].append(enc_msg[self.block_symbol:])

        return fec_msg

    def decode(self, enc_msg, dec_msg):

        msg_id = enc_msg[self.ID_IDX]
        fec_msg = enc_msg[self.SYM_IDX : ]

        # check for pkt with systematic idx
        if msg_id < self.alpha:
            slice = msg_id * self.block_symbol
            slice = enc_msg[self.IDX_IDX]
            fec_code.dec_msg[slice : slice + self.block_symbol] = fec_msg
            fec_code.recv_msg[msg_id] =  1
        elif msg_id >= self.alpha:
            if (fec_code.recv_msg[msg_id - self.alpha] == 0):
                for i in range(0, self.pkt_ln / self.block_symbol):
                    missing_symb = [0] * self.block_symbol
                    msg = []
                    msg_f = []
                    msg.insert(0, missing_symb)
                    #slice = i * self.block_symbol
                    #symbols = fec_msg[slice : slice + self.block_symbol]
                    msg.append(fec_msg[i])
                    msg_f = list(itertools.chain(*msg))
                    missing_symb = range(0, self.block_symbol)
                    self.code.decode(msg_f, missing_symb)

                    # add to the decode msg
                    slice_pkt = self.pkt_ln / self.block_symbol # block of symbols per fec pkt
                    slice = ((msg_id - self.alpha) * slice_pkt) + (self.block_symbol * i)
                    fec_code.dec_msg[slice : slice + self.block_symbol] = msg_f[:self.block_symbol]

                fec_code.recv_msg[msg_id - self.alpha] = 1# pkt 0 (src_symbols) has the info in pkt 0+alpha

        #if (any(fec_code.recv_msg == 0 for fec_code.recv_msg in fec_code.recv_msg)):
        if (0 in fec_code.recv_msg):
            return self.TRYING
        else:
            dec_msg.append(fec_code.dec_msg[:self.pkt_ln])
            return self.OK
