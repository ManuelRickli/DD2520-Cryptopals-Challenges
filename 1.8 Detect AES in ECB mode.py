from collections import defaultdict


def getNumberOfRepeatingBlocks(ciphertext):
	repetitions = defaultdict(lambda: -1)
	for i in range(0, len(ciphertext), 16):
		block = ciphertext[i:i + 16]
		repetitions[block] += 1

	return sum(repetitions.values())


if __name__ == '__main__':
	file = open("Input/1.8 Input", "r")
	bl = list()

	best = -1
	bestLine = ""

	for line in file:
		reps = getNumberOfRepeatingBlocks(line)
		if reps > best:
			best = reps
			bestLine = line

	print(bestLine)
