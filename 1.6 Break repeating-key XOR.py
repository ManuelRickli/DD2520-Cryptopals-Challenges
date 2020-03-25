from Methods import *


def hamminDistance(x, y):
	counter = 0
	for i in range(len(x)):
		counter += bin(x[i] ^ y[i]).count('1')

	return counter


def getKeySize(bl):
	distances = []
	for keysize in range(2, 40):
		b1 = bl[:keysize]
		b2 = bl[keysize:keysize * 2]
		b3 = bl[keysize * 2:keysize * 3]
		b4 = bl[keysize * 3:keysize * 4]

		d = (hamminDistance(b1, b2) + hamminDistance(b2, b3) + hamminDistance(b3, b4)) / (keysize * 3)
		distances.append((keysize, d))

	return sorted(distances, key=lambda tup: tup[1])


if __name__ == '__main__':

	file = open("Input/1.6 Input", "r")
	bl = list()

	for line in file:
		bl.append(binascii.a2b_base64(line))

	bl = b''.join(bl)

	# get most likely key sizes (ordered from most likely to least likely)
	keys = getKeySize(bl)

	bestScore = -1
	bestResult = ()

	for attempt in range(5):
		bestKeysize = keys[attempt][0]

		# divide original data into blocks of keysize
		newCipher = [bl[i:i + bestKeysize] for i in range(0, len(bl), bestKeysize)]

		# add padding to last block if necessary
		if len(newCipher[-1]) < bestKeysize:
			newCipher[-1] = newCipher[-1].ljust(bestKeysize, b'\0')

		# add every first byte of each block to the first block of the new blocks etc.
		newBlocks = [None] * bestKeysize
		for i in range(bestKeysize):
			newBlocks[i] = [item[i] for item in newCipher]

		# get the most likely key for each block and concatenate them to get the final key
		finalKey = list()
		for block in newBlocks:
			[c, t, s] = getBest(block)
			finalKey.append(c)

		print("Possible key " + str(attempt + 1) + ": " + ''.join(finalKey))

		decoded = repeat_xor(bl, finalKey)
		plainText = binascii.unhexlify(decoded)

		score = getScore(str(plainText))

		if score > bestScore:
			bestScore = score
			bestResult = (finalKey, plainText)

	print("Best result key: " + ''.join(bestResult[0]))
	print("Best result text: " + str(bestResult[1].decode()))
