import string
import nltk
import decoder
from nltk.util import ngrams
from nltk.corpus import reuters
from collections import Counter, defaultdict

def decrypt_caesar_cipher(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.lower() in string.ascii_lowercase:
            offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr(((ord(char) - offset - shift) % 26) + offset)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

# You need to download reuters and punkt once. If you've already run the script without these two lines commented out, comment them out before you run it again.
def bigram_model():
    #nltk.download('reuters')
    #nltk.download('punkt')

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

def get_text_bigram_score(text, bigram_model):
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
    model = bigram_model()
    best_score = float('-inf')
    best_shift = 0

    for shift in range(1, 26):
        plaintext = decrypt_caesar_cipher(ciphertext, shift)
        score = get_text_bigram_score(plaintext, model)
        if score > best_score:
            best_score = score
            best_shift = shift

    return decrypt_caesar_cipher(ciphertext, best_shift)
    
def main(): 
    ciphertext = "Jr znl or va fgevat naq va gvzr, naq va gur zvfg bs guvatf."
    plaintext = frequency_analysis(ciphertext)
    print(f"Ciphertext: {ciphertext}")
    print(f"Plaintext: {plaintext}")

if __name__ == "__main__":
    main()
