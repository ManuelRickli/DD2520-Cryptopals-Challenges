from Crypto.Cipher import AES
import binascii

obj = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)

file = open("Input/1.7 Input", "r")
bl = list()
for line in file:
	bl.append(binascii.a2b_base64(line))

bl = b''.join(bl)

plaintext = obj.decrypt(bl)

print(plaintext.decode())
# I'm back and I'm ringin' the bell...
