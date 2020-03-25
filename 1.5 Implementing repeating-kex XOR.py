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
		
	# 0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f
