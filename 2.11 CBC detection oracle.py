from Methods import *


def oracle(plaintext):
	x = randint(5, 10)
	plaintext = getRandomBytes(x) + plaintext + getRandomBytes(x)
	plaintext = addPadding(plaintext, AES.block_size)

	if randint(0, 1):
		return ecb_encrypt(getRandomBytes(AES.block_size), plaintext), 1
	else:
		return cbc_encrypt(getRandomBytes(AES.block_size), plaintext, getRandomBytes(AES.block_size)), 0


if __name__ == '__main__':
	input = open("Input/2.11 Input", "r")
	input = bytearray(''.join(input.readlines()), encoding="ascii")

	for i in range(400):
		[c, mode] = oracle(input)

		if getNumberOfRepeatingBlocks(c) > 0 and mode == 0:
			print("FAILURE!")
			exit(1)

	print("NOICE")
