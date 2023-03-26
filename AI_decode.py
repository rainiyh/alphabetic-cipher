import string
import random
import nltk
from nltk.util import ngrams
from nltk.corpus import reuters
from collections import defaultdict, Counter
import re

def decrypt_monoalphabetic(ciphertext, key):
    key_mapping = dict(zip(string.ascii_lowercase, key))
    decrypted_text = ""
    for char in ciphertext:
        if char.lower() in key_mapping:
            decrypted_char = key_mapping[char.lower()]
            decrypted_text += decrypted_char.upper() if char.isupper() else decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def digraph_model():
    nltk.download('reuters')

    model = defaultdict(lambda: defaultdict(lambda: 0))
    text = reuters.raw()
    text = re.sub(r"[^a-zA-Z]+", "", text).lower()
    digraphs = ngrams(text, 2)

    digraph_counts = Counter(digraphs)
    for digraph, count in digraph_counts.items():
        model[digraph[0]][digraph[1]] = count

    for first_char in model:
        total_count = float(sum(model[first_char].values()))
        for second_char in model[first_char]:
            model[first_char][second_char] /= total_count

    return model

def get_text_digraph_score(text, digraph_model):
    text = re.sub(r"[^a-zA-Z]+", "", text).lower()
    if len(text) < 2:
        return float('-inf')

    digraphs = ngrams(text, 2)
    score = 0
    for digraph in digraphs:
        score += digraph_model[digraph[0]][digraph[1]]

    return score

def hill_climbing(ciphertext, fitness_fn, iterations=20000):
    current_key = ''.join(random.sample(string.ascii_lowercase, len(string.ascii_lowercase)))
    current_score = fitness_fn(current_key)
    
    for _ in range(iterations):
        new_key = swap_two_letters(current_key)
        new_score = fitness_fn(new_key)

        if new_score > current_score:
            current_key = new_key
            current_score = new_score

    return current_key

def swap_two_letters(key):
    key = list(key)
    idx1, idx2 = random.sample(range(len(key)), 2)
    key[idx1], key[idx2] = key[idx2], key[idx1]
    return ''.join(key)

def frequency_analysis(ciphertext):
    model = digraph_model()

    def fitness_fn(key):
        plaintext = decrypt_monoalphabetic(ciphertext, key)
        return get_text_digraph_score(plaintext, model)

    best_key = hill_climbing(ciphertext, fitness_fn)
    return decrypt_monoalphabetic(ciphertext, best_key)

if __name__ == "__main__":
    text = open('ciphertext.txt').read().strip()
    text = re.sub(r'[^\w ]+', '', text)
    print(f"Ciphertext: {text}")
    plaintext = frequency_analysis(text)
    print(f"plaintext: {plaintext}")