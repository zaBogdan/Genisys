from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad, pad
from base64 import b64decode,b64encode

class DataEncryption:
    def encodeString(self, data, key):
        encryptedText = ''
        data = data.encode()
        key = key.encode()

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
        key = key.encode()
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decryptedString = unpad(cipher.decrypt(text), AES.block_size)
        return decryptedString.decode('utf8')

# enc = DataEncryption()
# data = 'Trying to not encrypt the text'
# key = 'abfc370ab633974ac2ace45cd55620a9'
# encryptedData = enc.encodeString(data,key)
# decryptedData = enc.decodeString(encryptedData,key)

# print("RawData: {}".format(data))
# print("EncryptedData: {}".format(encryptedData))
# print("Decoded data: {}".format(decryptedData))


