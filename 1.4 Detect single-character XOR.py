import binascii
from Methods import freqs


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
		result = [chr(byte ^ i) for byte in binascii.unhexlify(input)]

		results.append(''.join(result))

		if getScore(result) > s:
			s = getScore(result)
			bestChar = chr(i)
			resultingText = ''.join(result)

	return (bestChar, resultingText, s)


if __name__ == '__main__':

	bestScore = -1
	bestChar = ''
	bestText = ""
	bestLine = -1
	i = 0

	file = open("Input/1.4 Input", "r")
	for line in file:
		[c, t, s] = getBest(line.strip())
		if s > bestScore:
			bestScore = s
			bestChar = c
			bestText = t
			bestLine = i

		i += 1

	print(bestText)
	# Now that the party is jumping
	
	print(bestChar)
	# 5
	
	print(bestLine)
	# 170
