import sys
import random

def generate_code():
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	cipher_key = ''.join(random.sample(alphabet, len(alphabet)))
	cipher_map = dict(zip(alphabet, cipher_key))
	return cipher_map
	
def encrypt(message, code):
	encrypted_text = ''
	for char in message.lower():
		if char in code:
			encrypted_text += code[char]
		else:
			encrypted_text += char
	return encrypted_text
	
def decrypt(encrypted_text, code):
	decode = {v: k for k, v in code.items()}
	return encrypt(encrypted_text, decode)

def main():
	text = sys.argv[1]
	code = generate_code()
	encrypted_text = encrypt(text, code)
	print(encrypted_text)	
	print(decrypt(encrypted_text, code))

if (__name__ == "__main__"):
	main()
