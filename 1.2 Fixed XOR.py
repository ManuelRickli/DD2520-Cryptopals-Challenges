import codecs

n1 = "1c0111001f010100061a024b53535009181c"
n2 = "686974207468652062756c6c277320657965"

x1 = codecs.decode(n1, 'hex')
x2 = codecs.decode(n2, 'hex')

xor = [x1[i] ^ x2[i] for i in range(len(x1))]

print(codecs.encode(bytes(xor), 'hex').decode())