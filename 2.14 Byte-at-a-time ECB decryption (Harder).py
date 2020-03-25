from Methods import *

KEY = None
RANDOM_PREFIX = None


def oracle(plaintext):
	plaintext = RANDOM_PREFIX + plaintext
	plaintext += binascii.a2b_base64(
		"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n"
		"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n"
		"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n"
		"YnkK")
	plaintext = addPadding(plaintext, AES.block_size)

	return ecb_encrypt(KEY, plaintext)


if __name__ == '__main__':
	KEY = getRandomBytes(AES.block_size)
	RANDOM_PREFIX = getRandomBytes(randint(0, 256))

	# get the block size
	cipher_size_old = len(oracle(bytes()))
	block_size = -1

	for i in range(1, 1000):
		cipher_size = len(oracle(str.encode("A" * i)))
		if cipher_size != cipher_size_old:
			block_size = cipher_size - cipher_size_old
			break
		cipher_size_old = cipher_size

	# use 4 time block size because two blocks can get split up, which still leaves two blocks with only "A"s which
	# will be identically encrypted
	if getNumberOfRepeatingBlocks(oracle(str.encode("A" * block_size * 4))) > 0:
		print("ECB mode detected\n")
	else:
		print("No ECB mode")
		exit(1)

	# determine the length of the random-prefix
	index = -1
	buffer = -1
	# increase input length until two identical blocks can be found
	# -> random-prefix + input length will be aligned to the block size
	# the index of the first repeating block discovered will give the length of the random-prefix + buffer
	for k in range(block_size):
		y = oracle(str.encode("b" * k + "A" * block_size * 2))
		y = [y[i: i + block_size] for i in range(0, len(y), block_size)]

		result = {}
		i = 0
		for block in y:
			result[block] = -1, i
			i += 1

		for block_1 in y:
			for block_2 in y:
				if block_1 == block_2:
					result[block_1] = (result[block_1][0] + 1, result[block_1][1])

		index = -1
		for item in result.items():
			if item[1][0] > 0:
				index = item[1][1]

		if index != -1:
			buffer = k
			break

	rounded_text_size = len(oracle(str.encode("b" * buffer))) - block_size * (index - 1)
	prefix_size = len(oracle(str.encode("b" * buffer))) - rounded_text_size
	discovered_chars = ""

	for i in range(1, rounded_text_size):
		prefix = "A" * (rounded_text_size - i)
		block = oracle(str.encode("b" * buffer + prefix))[prefix_size:prefix_size + rounded_text_size]

		for char in range(256):
			cipher_block = oracle(str.encode("b" * buffer + prefix + discovered_chars + chr(char)))[
			               prefix_size:prefix_size + rounded_text_size]

			if block == cipher_block:
				discovered_chars += chr(char)
				break

	print(discovered_chars)
	# Rollin' in my 5.0...
