import hashlib
import time
import secrets
from injector import inject, singleton, Injector
class randomInterface:
    def __init__(self):
        pass
    def randomize_360(self, x, y, z):
        x=int(self.ord_str_gen(x))
        y=int(self.ord_str_gen(y))
        z=int(self.ord_str_gen(z))
        input_args = x ^ y ^ z
        hash_object = hashlib.sha256(str(input_args).encode())
        hash_digest = hash_object.hexdigest()
        hash_int = int(hash_digest, 16)
        return hash_int % 360

    def randomize_100(self, userID, lucky_seed):
        x = int(self.ord_str_gen(userID))
        y = int(self.ord_str_gen(lucky_seed))
        z = int(self.ord_str_gen(self.pseudo_random()))
        input_args = x ^ y ^ z
        hash_object = hashlib.sha256(str(input_args).encode())
        hash_digest = hash_object.hexdigest()
        hash_int = int(hash_digest, 16)
        return hash_int % 100


    def ord_str_gen(self,fort: str):
        out=""
        for i in fort:
            out+=str(ord(i))
        return out

    def pseudo_random(self):
        now = str(int(time.time())*1000 ^ int(secrets.randbits(128)))
        hash_obj = hashlib.sha256(now.encode())
        hex_digest = hash_obj.hexdigest()
        print("running pseudo random", hex_digest)
        return hex_digest
