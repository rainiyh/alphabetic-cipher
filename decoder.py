import random
import cracker
import string
import time
from itertools import permutations
from encoder import Alphabet

# Loads the words into a list to be checked against
def load_words():
	with open('words.txt', 'r') as f:
		word_list = [line.strip() for line in f.readlines()]
	return word_list
	
# Performant cracker
def crack():
	cracker.main()
	
def generate_random_combination():
	combination = ''
	for i in range(26):
		combination += random.choice(Alphabet.value)
	return combination
	
def test_random_combination(encoded, combination):
	decoded = ''
	for e in encoded:
		if e in Alphabet.value:
			decoded += combination[ord(e) - 97]
		else:
			decoded += ' '
	return decoded
	
def generate_freq_combination():
	words_list = ''.join(load_words())
	words_list = words_list.lower()
	return sort_freq(words_list)
	
def generate_encoded_letter_freq():
	encoded = cracker.load_ciphertext()
	return sort_freq(encoded)
	
def sort_freq(text):
	letter_freq = {}
	
	for letter in text:
		if letter in string.ascii_lowercase:
			if letter in letter_freq:
				letter_freq[letter] += 1
			else:
				letter_freq[letter] = 1
	
	sorted_letters = sorted(letter_freq.items(), key=lambda x: x[1], reverse=True)
	sorted_string = ''.join([pair[0] for pair in sorted_letters])
	
	return sorted_string
	
def moderate_force():
	permutations_list = list(permutations(generate_freq_combination()))
	permutations_list = sorted(permutations_list, key=lambda x: items.index(x[0]))
	
	for p in permutations_list:
		decoded = test_combination(encoded, p)
		if all(word in words_list for word in decoded.split()):
			print('Decoded text: ' + decoded)
			print('Combination: ' + combination)
			break

def bruteforce():
	encoded = cracker.load_ciphertext()
	words_list = load_words()
	tested = 0
	start_time = time.time()
	printed_time = start_time
	print("Brute forcing. This could take a while.")
	while True:
		combination = generate_random_combination()
		decoded = test_random_combination(encoded, combination)
		if all(word in words_list for word in decoded.split()):
			print('Decoded text: ' + decoded)
			print('Combination: ' + combination)
			break
		else:
			tested += 1
		if (tested % 1000 == 0):
			if (time.time() - printed_time > 5):
				print_time = time.time() - start_time
				printed_time = time.time()
				print(f"Seconds elapsed: {print_time}\nCombinations tried: {tested}")

# Do the decoding here
def main():
	start_time = time.time()
	crack()
	end_time = time.time()
	execution_time = end_time - start_time
	print(f"Execution time: {execution_time} seconds")
	#bruteforce()

if (__name__ == "__main__"):
	main()
