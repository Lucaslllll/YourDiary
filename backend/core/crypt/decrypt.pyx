from cpython cimport bool
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

cpdef bytes decrypt_text(bytes key, bytes ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    cdef bytes padded_plaintext = cipher.decrypt(ciphertext)
    cdef bytes plaintext = unpad(padded_plaintext, AES.block_size)
    
    return plaintext