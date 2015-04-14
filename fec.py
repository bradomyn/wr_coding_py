import sys
sys.path.append('./rs/')

from rs_code import rs_code

class fec_code:

    def __init__(self, code_id):
        self.pkt = 4
        self.code_id = 1 # RS = 1 LDPC = 2 LT = 3
        self.pkt_id = 0
        self.block_symbol = 128
        self.pkt_ln = 512
        self.block_ln = 1024

        if code_id == 1:
            self.code = rs_code()

    def get_data(self, msg_file):

        f = open(msg_file,'r')
        msg_input = f.read(self.block_ln)
        msg_int_byte = [0] * len(msg_input)
        for i in range(0, len(msg_input)):
            msg_int_byte[i] = ord(msg_input[i])

        return msg_int_byte

    def encode(self, msg):
        fec_msg = [[] for l in range(0, self.pkt) ]

        for i in range (0,self.pkt/2 ):
            enc_msg = self.code.encode(msg[i * self.pkt_ln : self.pkt_ln * (i + 1)])

            j = i + 2
            fec_msg[i].append(self.code_id)
            self.pkt_id = i
            fec_msg[i].append(self.pkt_id)
            b_symbol = self.block_symbol * i
            fec_msg[i].append(b_symbol)
            fec_msg[i].append(enc_msg[0 : self.pkt_ln/2])

            fec_msg[j].append(self.code_id)
            self.pkt_id = j
            fec_msg[j].append(self.pkt_id)
            b_symbol = self.block_symbol * j
            fec_msg[j].append(b_symbol)
            fec_msg[j].append(enc_msg[self.pkt_ln/2: ])

        return fec_msg


