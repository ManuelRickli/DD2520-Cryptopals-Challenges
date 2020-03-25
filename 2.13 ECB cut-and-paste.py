from Methods import *

uid = -1


def profile_for(mail):
	global uid
	uid += 1

	mail = mail.replace("=", "").replace("&", "")
	return encrypt("mail=" + mail + "&uid=" + str(uid) + "&role=user")


def parse(encrypted):
	encoded = decrypt(encrypted).decode()
	user = {}

	for amp in encoded.split("&"):
		eq = amp.split("=")
		user[eq[0]] = eq[1]

	user["encoded"] = encoded

	return user


def encrypt(user):
	global key
	return ecb_encrypt(key, addPadding(str.encode(user), AES.block_size))


def decrypt(ciphertext):
	global key
	plaintext = ecb_decrypt(key, ciphertext)
	return removePadding(plaintext)


if __name__ == '__main__':
	global key
	key = getRandomBytes(AES.block_size)

	# get length of fixed characters and construct mail address that aligns everything after "...role=" to the block size
	fixed_length = len("mail=&uid=0&role=")
	block_aligned_size = ((fixed_length // AES.block_size) + 1) * AES.block_size
	arbitrary_mail = "A" * (block_aligned_size - fixed_length)

	# the prefix contains a ciphertext that is block aligned with the role -> decrypts to "mail=A..&uid=1&role="
	prefix = profile_for(arbitrary_mail)[:block_aligned_size]

	# the same again, but aligned to the mail
	fixed_length = len("mail=")
	block_aligned_size = ((fixed_length // AES.block_size) + 1) * AES.block_size
	arbitrary_mail = "A" * (block_aligned_size - fixed_length)

	# construct a block sized string with padding which contains "admin"
	admin = addPadding(str.encode("admin"), AES.block_size).decode()

	# the postfix contains ciphertext which is constructed with the above admin padded string -> decrypts to "admin"
	postfix = profile_for(arbitrary_mail + admin)[block_aligned_size:block_aligned_size + AES.block_size]

	# parsing the prefix concatenated with the postfix yields "mail=A..&uid=1&role=admin"
	print(parse(prefix + postfix)["encoded"])
