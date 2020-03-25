from Methods import *

KEY = None


def oracle(plaintext):
	plaintext += binascii.a2b_base64(
		"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK")
	plaintext = addPadding(plaintext, AES.block_size)

	return ecb_encrypt(KEY, plaintext)


if __name__ == '__main__':
	KEY = getRandomBytes(AES.block_size)

	block_size = 0
	cipher_text_size = 0
	cipher_size_old = len(oracle(bytes()))

	for i in range(1, 1000):
		cipher_size = len(oracle(str.encode("A" * i)))
		if cipher_size_old != cipher_size:
			block_size = cipher_size - cipher_size_old
			cipher_text_size = cipher_size - i
			break
		cipher_size_old = cipher_size

	if getNumberOfRepeatingBlocks(oracle(str.encode("A" * block_size))) > 0:
		print("ECB mode detected\n")
	else:
		print("No ECB mode")
		exit(1)

	discovered_chars = ""
	rounded_text_size = block_size * ((cipher_text_size // block_size) + 1)

	for i in range(1, rounded_text_size):
		prefix = "A" * (rounded_text_size - i)
		block = oracle(str.encode(prefix))[:rounded_text_size]

		for char in range(256):
			cipher_block = oracle(str.encode(prefix + discovered_chars + chr(char)))[:rounded_text_size]

			if block == cipher_block:
				discovered_chars += chr(char)
				break

	print(discovered_chars)
