import binascii


def xor(text, key):
	result = list()

	for i in range(len(text)):
		k = key[i % len(key)]

		result.append(ord(text[i]) ^ ord(k))

	return binascii.hexlify(bytes(result))

if __name__ == '__main__':
	s = {"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"}

	for text in s:
		print(xor(text, "ICE").decode())
