import hashlib
import time
from injector import inject, singleton, Injector
class randomInterface:
    def __init__(self):
        pass
    def randomize(self,x,y,z):
        x=int(self.ord_str_gen(x))
        y=int(self.ord_str_gen(y))
        z=int(self.ord_str_gen(z))
        input_args = x ^ y ^ z
        hash_object = hashlib.sha256(str(input_args).encode())
        hash_digest = hash_object.hexdigest()
        hash_int = int(hash_digest, 16)
        angle = hash_int % 360
        return angle
    def ord_str_gen(self,fort: str):
        out=""
        for i in fort:
            out+=str(ord(i))
        return out
    def pseudo_random(self):
        now = str(time.time())
        hash_obj = hashlib.sha256(now.encode())
        hex_digest = hash_obj.hexdigest()
        return hex_digest
