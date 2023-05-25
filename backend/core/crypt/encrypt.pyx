from cpython cimport bool
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

cpdef bytes encrypt_text(bytes key, bytes plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    cdef bytes padded_plaintext = pad(plaintext, AES.block_size)
    cdef bytes ciphertext = cipher.encrypt(padded_plaintext)
    
    return ciphertext