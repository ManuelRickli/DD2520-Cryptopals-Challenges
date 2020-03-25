from Methods import *


def ecb_encrypt(key, plaintext):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.encrypt(plaintext)


def ecb_decrypt(key, ciphertext):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.decrypt(ciphertext)


def cbc_encrypt(key, plaintext, iv):
	plaintext = addPadding(plaintext, AES.block_size)
	ciphertext = bytearray(len(plaintext))
	previous_block = iv

	for i in range(0, len(plaintext), AES.block_size):
		ciphertext[i:i + AES.block_size] = ecb_encrypt(key, xor(plaintext[i: i + AES.block_size], previous_block))

		previous_block = ciphertext[i:i + AES.block_size]

	return bytes(ciphertext)


def cbc_decrypt(key, ciphertext, iv):
	plaintext = bytearray(len(ciphertext))
	previous_block = iv

	for i in range(0, len(ciphertext), AES.block_size):
		plaintext[i:i + AES.block_size] = xor(previous_block, ecb_decrypt(key, ciphertext[i: i + AES.block_size]))

		previous_block = ciphertext[i:i + AES.block_size]

	return removePadding(plaintext)


if __name__ == '__main__':
	file = open("Input/2.10 Input", "r")
	bl = list()
	for line in file:
		bl.append(binascii.a2b_base64(line))

	bl = b''.join(bl)

	key = "YELLOW SUBMARINE"
	iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

	print(cbc_decrypt(key, bl, iv).decode())
