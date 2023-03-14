import sys
import random

# USAGE: python3 encoder.py "some silly message that will be displayed encoded then decoded"

# Generates an alphabetic cipher. Each letter in the alphabet is mapped to another unique letter.
def generate_code():
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	cipher_key = ''.join(random.sample(alphabet, len(alphabet)))
	cipher_map = dict(zip(alphabet, cipher_key))
	return cipher_map
	
# Encrypt a message using a code as generated in generate_code. Pass in a string and a dictionary, with the dictionary mapping a letter to another letter.
def encrypt(message, code):
	encrypted_text = ''
	for char in message.lower():
		if char in code:
			encrypted_text += code[char]
		else:
			encrypted_text += char
	return encrypted_text
	
# Inverts the encryption. Otherwise, identical usage to encrypt().
def decrypt(encrypted_text, code):
	decode = {v: k for k, v in code.items()}
	return encrypt(encrypted_text, decode)

# Send a message from CLI. The script will display it encoded and then decoded.
def main():
	text = sys.argv[1]

	print("The plaintext to encode is: ", text)

	code = generate_code()

	print("It will be encoded using the following key:")
	print(code)

	encrypted_text = encrypt(text, code)

	print("The ciphertext is: ", encrypted_text)

	print("It can be decoded using the same key. Here is the decrypted text: ", decrypt(encrypted_text, code))

	# print(decrypt(encrypted_text, code))

if (__name__ == "__main__"):
	main()
