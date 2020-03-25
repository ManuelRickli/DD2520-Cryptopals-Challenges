from Methods import removePadding2

if __name__ == '__main__':
	s1 = "ICE ICE BABY\x04\x04\x04\x04"
	s2 = "ICE ICE BABY\x05\x05\x05\x05"
	s3 = "ICE ICE BABY\x01\x02\x03\x04"

	print(removePadding2(s1.encode())) # b'ICE ICE BABY
	# print(removePadding2(s2.encode())) # AssertionError: Bad padding!
	# print(removePadding2(s3.encode())) # AssertionError: Bad padding!
