from gf import *

class rs_code:
    k = 128
    n = 256
    n_k = 0

    def __init__(self):
        rs_code.n_k = self.n - self.k

    def print_poly(self, name, poly):
        print name, ": ",
        for i in range(0,len(poly)):
            print hex(poly[i]),
        print "\n"

    # Encode RS
    def encode(self, msg_in):
       nsym = rs_code.n_k
       gen = rs_generator_poly(nsym)
       msg_out = [0] * (len(msg_in) + nsym)
       for i in range(0, len(msg_in)):
          msg_out[i] = msg_in[i]
       for i in range(0, len(msg_in)):
          coef = msg_out[i]
          if coef != 0:
             for j in range(0, len(gen)):
                msg_out[i+j] ^= gf_mul(gen[j], coef)
       for i in range(0, len(msg_in)):
          msg_out[i] = msg_in[i]
       return msg_out

    def calc_syndromes(self, msg):
       nsym = rs_code.n_k
       synd = [0] * nsym
       for i in range(0, nsym):
          synd[i] = gf_poly_eval(msg, gf_exp[i])
       return synd

    def decode(self, msg, pos):
       nsym = rs_code.n_k
       #syndrome calculation
       synd = rs_code.calc_syndromes(self, msg)

       # calculate error locator polynomial
       q = [1]
       for i in range(0, len(pos)):
          x = gf_exp[len(msg)-1-pos[i]]
          q = gf_poly_mul(q, [x,1])

       # calculate error evaluator polynomial
       p = synd[0:len(pos)]
       p.reverse()
       p = gf_poly_mul(p, q)

       p = p[len(p)-len(pos):len(p)]
       # formal derivative of error locator eliminates even terms
       qprime = q[len(q)&1:len(q):2]
       # compute corrections
       for i in range(0, len(pos)):
          x = gf_exp[pos[i]+256-len(msg)]
          y = gf_poly_eval(p, x)
          z = gf_poly_eval(qprime, gf_mul(x,x))
          msg[pos[i]] ^= gf_div(y, gf_mul(x,z))
