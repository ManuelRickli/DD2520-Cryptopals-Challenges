from Methods import *

KEY = ""
IV = ""


def oracle(plaintext):
	plaintext = plaintext.replace(";", "\";\"").replace("=", "\"=\"")
	plaintext = "comment1=cooking%20MCs;userdata=" + plaintext + ";comment2=%20like%20a%20pound%20of%20bacon"

	return cbc_encrypt(KEY, plaintext.encode(), IV)


def checkAdmin(ciphertext):
	return b";admin=true;" in cbc_decrypt(KEY, ciphertext, IV)


if __name__ == '__main__':
	KEY = getRandomBytes(AES.block_size)
	IV = getRandomBytes(AES.block_size)

	offset = 32

	block1 = "A" * AES.block_size
	block2 = "AadminAtrueA"
	cipher = bytearray(oracle(block1 + block2))

	cipher[offset] = cipher[offset] ^ (ord("A") ^ ord(";"))
	cipher[offset + 6] = cipher[offset + 6] ^ (ord("A") ^ ord("="))
	cipher[offset + 11] = cipher[offset + 11] ^ (ord("A") ^ ord(";"))

	if checkAdmin(bytes(cipher)):
		print("yay")
	else:
		print("nay")
