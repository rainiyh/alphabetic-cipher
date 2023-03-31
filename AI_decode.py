import string
import nltk
import time
from nltk.util import ngrams
from nltk.corpus import reuters
from collections import Counter, defaultdict
nltk.download('reuters')
nltk.download('punkt')


def decrypt_cipher(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.lower() in string.ascii_lowercase:
            offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr(((ord(char) - offset - shift) % 26) + offset)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def Model():
 
    model = defaultdict(lambda: defaultdict(lambda: 0))
    sentences = reuters.sents()
    bigrams = []

    for sentence in sentences:
        sentence = [word.lower() for word in sentence if word.isalpha()]
        bigrams.extend(list(ngrams(sentence, 2)))

    bigram_counts = Counter(bigrams)
    for bigram, count in bigram_counts.items():
        model[bigram[0]][bigram[1]] = count

    for first_word in model:
        total_count = float(sum(model[first_word].values()))
        for second_word in model[first_word]:
            model[first_word][second_word] /= total_count

    return model

def Score(text, bigram_model):
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalpha()]

    if len(words) < 2:
        return float('-inf')

    bigrams = list(ngrams(words, 2))
    score = 0
    for bigram in bigrams:
        score += bigram_model[bigram[0]][bigram[1]]

    return score

def frequency_analysis(ciphertext):
    model = Model()
    best_score = float('-inf')
    best_shift = 0

    for shift in range(1, 26):
        plaintext = decrypt_cipher(ciphertext, shift)
        score = Score(plaintext, model)
        if score > best_score:
            best_score = score
            best_shift = shift

    return decrypt_cipher(ciphertext, best_shift)
    
def main():
    start_time = time.time()
    ciphertext = "olssv P ht h yviva. Upjl av tlla fvb."
    print(f"Ciphertext: {ciphertext}")
    plaintext = frequency_analysis(ciphertext)
    print(f"Plaintext: {plaintext}")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

if __name__ == "__main__":
    main()