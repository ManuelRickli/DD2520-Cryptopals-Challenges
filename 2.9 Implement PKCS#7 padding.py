def addPadding(s, padding):
	blocks = list()
	blocks.append(s[:20])

	for i in range(1, len(s) // padding + 1):
		blocks.append(s[padding * i:padding * i + padding])

	if len(blocks[-1]) < padding:
		diff = padding - len(blocks[-1])
		blocks[-1] += str(bytes([diff]).decode()) * diff

	return blocks

def removePadding(s):
	x = s[-1]
	if not isinstance(x, int):
		return s
	else:
		for i in range(len(s) - 1, len(s) - x - 1, -1):
			if s[i] != x:
				return s

		return s[:len(s) - x - 1]


if __name__ == '__main__':
	s = "YELLOW SUBMARINEssssssssssssssssssssssssssssssssssssssssssssssss"
	padding = 20

	blocks = addPadding(s, padding)

	print(blocks)
