import binascii
from collections import defaultdict
from random import randint

from Crypto.Cipher import AES

freqs = {
	'a': 0.0651738,
	'b': 0.0124248,
	'c': 0.0217339,
	'd': 0.0349835,
	'e': 0.1041442,
	'f': 0.0197881,
	'g': 0.0158610,
	'h': 0.0492888,
	'i': 0.0558094,
	'j': 0.0009033,
	'k': 0.0050529,
	'l': 0.0331490,
	'm': 0.0202124,
	'n': 0.0564513,
	'o': 0.0596302,
	'p': 0.0137645,
	'q': 0.0008606,
	'r': 0.0497563,
	's': 0.0515760,
	't': 0.0729357,
	'u': 0.0225134,
	'v': 0.0082903,
	'w': 0.0171272,
	'x': 0.0013692,
	'y': 0.0145984,
	'z': 0.0007836,
	' ': 0.1918182
}


def getScore(text):
	score = 0
	for i in text:
		if i in freqs:
			score += freqs[i]

	return score


def getBest(input):
	results = list()

	s = -1
	bestChar = ''
	resultingText = ""

	for i in range(256):
		result = [chr(byte ^ i) for byte in input]

		results.append(''.join(result))

		if getScore(result) > s:
			s = getScore(result)
			bestChar = chr(i)
			resultingText = ''.join(result)

	return bestChar, resultingText, s


def xor(word1, word2):
	assert len(word1) == len(word2)
	x = [word1[i] ^ word2[i] for i in range(len(word1))]
	return bytes(x)


def repeat_xor(text, key):
	result = list()

	for i in range(len(text)):
		k = key[i % len(key)]

		result.append(text[i] ^ ord(k))

	return binascii.hexlify(bytes(result))


def getNumberOfRepeatingBlocks(ciphertext):
	repetitions = defaultdict(lambda: -1)
	for i in range(0, len(ciphertext), 16):
		block = ciphertext[i:i + 16]
		repetitions[block] += 1

	return sum(repetitions.values())


def addPadding(s, padding):
	blocks = list()
	blocks.append(s[:padding])

	for i in range(1, len(s) // padding):
		blocks.append(s[padding * i:padding * i + padding])

	if len(s) > padding and len(s) % padding != 0:
		blocks.append(s[-(len(s) % padding):])

	if len(blocks[-1]) < padding:
		diff = padding - len(blocks[-1])
		blocks[-1] += bytes([diff]) * diff

	return b''.join(blocks)


def removePadding(s):
	x = s[-1]
	if not isinstance(x, int):
		return s
	else:
		for i in range(len(s) - 1, len(s) - x - 1, -1):
			if s[i] != x:
				return s

		return s[:len(s) - x]

def removePadding2(s):
	x = s[-1]
	if not isinstance(x, int):
		return s
	else:
		for i in range(len(s) - 1, len(s) - x - 1, -1):
			assert s[i] == x, "Bad padding!"

		return s[:len(s) - x]


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


def getRandomBytes(n):
	result = bytearray(n)
	for i in range(n):
		result[i] = randint(0, 255)

	return bytes(result)
