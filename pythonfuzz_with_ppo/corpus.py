# import os
# import random
# import hashlib

# import dictionnary

# try:
#     from random import _randbelow
# except ImportError:
#     from random import _inst
#     _randbelow = _inst._randbelow

# INTERESTING8 = [-128, -1, 0, 1, 16, 32, 64, 100, 127]
# INTERESTING16 = [0, 128, 255, 256, 512, 1000, 1024, 4096, 32767, 65535]
# INTERESTING32 = [0, 1, 32768, 65535, 65536, 100663045, 2147483647, 4294967295]

# class Corpus(object):
#     def __init__(self, dirs=None, max_input_size=1024, dict_path=None):
#         self._inputs = []
#         self._dict = dictionnary.Dictionary(dict_path)
#         self._max_input_size = max_input_size
#         self._dirs = dirs if dirs else []
#         for i, path in enumerate(dirs):
#             if i == 0 and not os.path.exists(path):
#                 os.mkdir(path)

#             if os.path.isfile(path):
#                 self._add_file(path)
#             else:
#                 for i in os.listdir(path):
#                     fname = os.path.join(path, i)
#                     if os.path.isfile(fname):
#                         self._add_file(fname)
#         self._seed_run_finished = not self._inputs
#         self._seed_idx = 0
#         self._save_corpus = dirs and os.path.isdir(dirs[0])

#     def _add_file(self, path):
#         with open(path, 'rb') as f:
#             self._inputs.append(bytearray(f.read()))

#     @property
#     def length(self):
#         return len(self._inputs)

#     @staticmethod
#     def _rand(n):
#         if n < 2:
#             return 0
#         return _randbelow(n)

#     # Exp2 generates n with probability 1/2^(n+1).
#     @staticmethod
#     def _rand_exp():
#         rand_bin = bin(random.randint(0, 2**32-1))[2:]
#         rand_bin = '0'*(32 - len(rand_bin)) + rand_bin
#         count = 0
#         for i in rand_bin:
#             if i == '0':
#                 count +=1
#             else:
#                 break
#         return count

#     @staticmethod
#     def _choose_len(n):
#         x = Corpus._rand(100)
#         if x < 90:
#             return Corpus._rand(min(8, n)) + 1
#         elif x < 99:
#             return Corpus._rand(min(32, n)) + 1
#         else:
#             return Corpus._rand(n) + 1

#     @staticmethod
#     def copy(src, dst, start_source, start_dst, end_source = None, end_dst = None):
#         end_source = len(src) if end_source is None else end_source
#         end_dst = len(dst) if end_dst is None else end_dst
#         byte_to_copy = min(end_source - start_source, end_dst - start_dst)
#         dst[start_dst:start_dst + byte_to_copy] = src[start_source:start_source+byte_to_copy]

#     def put(self, buf):
#         self._inputs.append(buf)
#         if self._save_corpus:
#             m = hashlib.sha256()
#             m.update(buf)
#             fname = os.path.join(self._dirs[0], m.hexdigest())
#             with open(fname, 'wb') as f:
#                 f.write(buf)

#     def generate_input(self, position = 5):
#         if not self._seed_run_finished:
#             next_input = self._inputs[self._seed_idx]
#             self._seed_idx += 1
#             if self._seed_idx >= len(self._inputs):
#                 self._seed_run_finished = True
#             return next_input

#         buf = self._inputs[self._rand(len(self._inputs))]
#         return self.mutate(buf, position)

#     def mutate(self, buf, position):
#         res = buf.ljust(1024, b'\x00')
#         x = self._rand(15)
#         if x == 0:
#             # Remove a byte at position
#             if len(res) > 1:
#                 res.pop(position)
#         elif x == 1:
#             # Insert a random byte at position
#             res.insert(position, self._rand(256))
#         elif x == 2:
#             # Duplicate byte at position
#             if len(res) < 1024:
#                 res.insert(position, res[position])
#         elif x == 3:
#             # Copy byte to another position
#             dst = self._rand(len(res))
#             res[dst] = res[position]
#         elif x == 4:
#             # Bit flip
#             res[position] ^= 1 << self._rand(8)
#         elif x == 5:
#             # Set a byte to a random value
#             res[position] = self._rand(256)
#         elif x == 6:
#             # Swap with another byte
#             dst = self._rand(len(res))
#             res[position], res[dst] = res[dst], res[position]
#         elif x == 7:
#             # Add/subtract a random value
#             res[position] = (res[position] + self._rand(256)) % 256
#         elif x == 8 and position < len(res) - 1:
#             # Modify uint16 at position
#             v = self._rand(2**16)
#             res[position] = (res[position] + (v & 0xFF)) % 256
#             res[position + 1] = (res[position + 1] + ((v >> 8) & 0xFF)) % 256
#         elif x == 9 and position < len(res) - 3:
#             # Modify uint32 at position
#             v = self._rand(2**32)
#             for k in range(4):
#                 res[position + k] = (res[position + k] + ((v >> (8 * k)) & 0xFF)) % 256
#         elif x == 10 and position < len(res) - 7:
#             # Modify uint64 at position
#             v = self._rand(2**64)
#             for k in range(8):
#                 res[position + k] = (res[position + k] + ((v >> (8 * k)) & 0xFF)) % 256
#         elif x == 11:
#             # Replace with an interesting byte
#             res[position] = INTERESTING8[self._rand(len(INTERESTING8))] % 256
#         elif x == 12 and position < len(res) - 1:
#             # Replace uint16 with an interesting value
#             v = random.choice(INTERESTING16)
#             res[position] = v & 0xFF
#             res[position + 1] = (v >> 8) & 0xFF
#         elif x == 13 and position < len(res) - 3:
#             # Replace uint32 with an interesting value
#             v = random.choice(INTERESTING32)
#             for k in range(4):
#                 res[position + k] = (v >> (8 * k)) & 0xFF
#         elif x == 14:
#             # Replace an ASCII digit at position
#             if ord('0') <= res[position] <= ord('9'):
#                 new_digit = res[position]
#                 while new_digit == res[position]:
#                     new_digit = self._rand(10) + ord('0')
#                 res[position] = new_digit
#         if len(res) > self._max_input_size:
#             res = res[:self._max_input_size]
#         return res
import os
import random
import hashlib
import dictionnary

class Corpus:
    INTERESTING8 = [-128, -1, 0, 1, 16, 32, 64, 100, 127]
    INTERESTING16 = [0, 128, 255, 256, 512, 1000, 1024, 4096, 32767, 65535]
    INTERESTING32 = [0, 1, 32768, 65535, 65536, 100663045, 2147483647, 4294967295]

    def __init__(self, dirs=None, max_input_size=1024, dict_path=None):
        self._inputs = []
        self._dict = dictionnary.Dictionary(dict_path)
        self._max_input_size = max_input_size
        self._dirs = dirs or []
        
        if self._dirs:
            os.makedirs(self._dirs[0], exist_ok=True)

        for path in self._dirs:
            if os.path.isfile(path):
                self._add_file(path)
            else:
                with os.scandir(path) as it:
                    for entry in it:
                        if entry.is_file():
                            self._add_file(entry.path)

        self._seed_run_finished = not self._inputs
        self._seed_idx = 0
        self._save_corpus = bool(dirs and os.path.isdir(dirs[0]))
        self._inputs.append(bytearray(os.urandom(1000)))

    def _add_file(self, path):
        with open(path, 'rb') as f:
            self._inputs.append(bytearray(f.read()))

    @property
    def length(self):
        return len(self._inputs)

    @staticmethod
    def _rand(n):
        return random.randrange(n) if n > 1 else 0

    @staticmethod
    def _rand_exp():
        return (random.getrandbits(32) & -random.getrandbits(32)).bit_length()

    @staticmethod
    def _choose_len(n):
        x = Corpus._rand(100)
        return Corpus._rand(min((8, 32, n)[(x > 90) + (x > 99)], n)) + 1

    @staticmethod
    def copy(src, dst, start_source, start_dst, end_source=None, end_dst=None):
        dst[start_dst:start_dst + min((end_source or len(src)) - start_source, (end_dst or len(dst)) - start_dst)] = \
            src[start_source:end_source]

    def put(self, buf):
        self._inputs.append(buf)
        self._seed_run_finished = False
        if self._save_corpus:
            fname = os.path.join(self._dirs[0], hashlib.sha256(buf).hexdigest())
            with open(fname, 'wb') as f:
                f.write(buf)

    def get_input(self):
        return self._inputs[self._seed_idx]
    
    def generate_input(self, position=5):
        if not self._seed_run_finished:
            next_input = self._inputs[self._seed_idx]
            self._seed_idx += 1
            self._seed_run_finished = self._seed_idx >= len(self._inputs)
            return next_input
        return self.mutate(self._inputs[self._rand(len(self._inputs))], position)

    def mutate(self, buf, position = 0):
        position = min(position, len(buf) - 1)        
        mutated = False
        while not mutated:
            x = self._rand(17)
            if x == 0 and len(buf) > 1:
                del buf[position]
                mutated = True
            elif x == 1 and len(buf) < self._max_input_size:
                buf.insert(position, self._rand(256))
                mutated = True
            elif x == 2 and len(buf) < self._max_input_size:
                buf.insert(position, buf[position])
                mutated = True
            elif x == 3:
                buf[self._rand(len(buf))] = buf[position]
                mutated = True
            elif x == 4:
                buf[position] ^= 1 << self._rand(8)
                mutated = True
            elif x == 5:
                buf[position] = self._rand(256)
                mutated = True
            elif x == 6:
                dst = self._rand(len(buf))
                buf[position], buf[dst] = buf[dst], buf[position]
                mutated = True
            elif x == 7:
                buf[position] = (buf[position] + self._rand(256)) % 256
                mutated = True
            elif x == 8 and position < len(buf) - 1:
                v = self._rand(2**16)
                buf[position] = (buf[position] + (v & 0xFF)) % 256
                buf[position + 1] = (buf[position + 1] + ((v >> 8) & 0xFF)) % 256
                mutated = True
            elif x == 9 and position < len(buf) - 3:
                v = self._rand(2**32)
                for k in range(4):
                    buf[position + k] = (buf[position + k] + ((v >> (8 * k)) & 0xFF)) % 256
                mutated = True
            elif x == 10 and position < len(buf) - 7:
                v = self._rand(2**64)
                for k in range(8):
                    buf[position + k] = (buf[position + k] + ((v >> (8 * k)) & 0xFF)) % 256
                mutated = True
            elif x == 11:
                buf[position] = self.INTERESTING8[self._rand(len(self.INTERESTING8))] % 256
                mutated = True
            elif x == 12 and position < len(buf) - 1:
                v = random.choice(self.INTERESTING16)
                buf[position:position + 2] = v.to_bytes(2, 'little')
                mutated = True
            elif x == 13 and position < len(buf) - 3:
                v = random.choice(self.INTERESTING32)
                buf[position:position + 4] = v.to_bytes(4, 'little')
                mutated = True
            elif x == 14 and ord('0') <= buf[position] <= ord('9'):
                buf[position] = self._rand(10) + ord('0') if buf[position] != ord('9') else ord('8')
                mutated = True
            elif x == 15 and len(buf) > 2:
                del buf[position:position + 2]
                mutated = True
            elif x == 16 and len(buf) > 4:
                del buf[position:position + 4]
                mutated = True

        return buf[:self._max_input_size]
