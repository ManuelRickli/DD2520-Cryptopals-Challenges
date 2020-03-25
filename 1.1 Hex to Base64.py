import codecs
import binascii

input = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

print(codecs.encode(codecs.decode(input, 'hex'), 'base64').decode())
# SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

print(binascii.a2b_hex(input).decode())
# I'm killing your brain like a poisonous mushroom


