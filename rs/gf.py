import sys

# GF Arithmetic
gf_exp = [0] * 512 # Create list of 512 elements. In Python 2.6+, consider using bytearray
gf_log = [0] * 256
gf_exp[0] = 1
x = 1
for i in range(1,255):
   x <<= 1
   if x & 0x100:
      x ^= 0x11d
   gf_exp[i] = x
   gf_log[x] = i
for i in range(255,512):
   gf_exp[i] = gf_exp[i-255]
gf_log[gf_exp[255]] = 255 # Set last missing elements in gf_log[]

def gf_mul(x,y):
   if x==0 or y==0:
      return 0
   return gf_exp[gf_log[x] + gf_log[y]]

def gf_div(x,y):
   if y==0:
      raise ZeroDivisionError()
   if x==0:
      return 0
   return gf_exp[gf_log[x] + 255 - gf_log[y]]

def gf_poly_scale(p,x):
   r = [0] * len(p)
   for i in range(0, len(p)):
      r[i] = gf_mul(p[i], x)
   return r

def gf_poly_add(p,q):
   r = [0] * max(len(p),len(q))
   for i in range(0,len(p)):
      r[i+len(r)-len(p)] = p[i]
   for i in range(0,len(q)):
      r[i+len(r)-len(q)] ^= q[i]
   return r

def gf_poly_mul(p,q):
   r = [0] * (len(p)+len(q)-1)
   for j in range(0, len(q)):
      for i in range(0, len(p)):
         r[i+j] ^= gf_mul(p[i], q[j])
   return r

def gf_poly_eval(p,x):
   y = p[0]
   for i in range(1, len(p)):
      y = gf_mul(y,x) ^ p[i]
   return y

# RS Generator Poly
def rs_generator_poly(nsym):
   g = [1]
   for i in range(0,nsym):
      g = gf_poly_mul(g, [1, gf_exp[i]])
      #g = gf_poly_mul(g, [1, i])

   return g

