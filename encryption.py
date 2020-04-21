from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad, pad
from base64 import b64decode,b64encode
from hashlib import md5

class DataEncryption:
    def encodeString(self, data, key):
        encryptedText = ''
        data = data.encode()
        key = md5(key.encode()).hexdigest().encode()

        cipher = AES.new(key, AES.MODE_CBC)
        encryptedText = cipher.encrypt(pad(data, AES.block_size))

        text = b64encode(encryptedText).decode('utf8')
        iv = b64encode(cipher.iv).decode('utf8')
        data = ''.join([iv, ':',text])
        return data

    def decodeString(self, data,key):
        decryptedString = ''
        data = data.split(':')
        iv = b64decode(data[0])
        text = b64decode(data[1])
        key = md5(key.encode()).hexdigest().encode()
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decryptedString = unpad(cipher.decrypt(text), AES.block_size)
        return decryptedString.decode('utf8')



