import sys
import random

# USAGE: python3 encoder.py "some silly message that will be displayed encoded then decoded"

class Alphabet:
	value = 'abcdefghijklmnopqrstuvwxyz'

# Generates an alphabetic cipher. Each letter in the alphabet is mapped to another unique letter.
def generate_code():
	alphabet = Alphabet.value
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

	print("The plaintext to encrypt is: ", text)

	code = generate_code()

	print("\nIt will be encrypted using the following key:")
	print(code, "\n")

	encrypted_text = encrypt(text, code)

	print("\nThe ciphertext is: ", encrypted_text)

	with open('ciphertext.txt', 'w') as f:
		print(encrypted_text, file=f)

	print("\nIt can be decrypted using the same key. Here is the decrypted text: ", decrypt(encrypted_text, code))

	# print(decrypt(encrypted_text, code))

if (__name__ == "__main__"):
	main()
