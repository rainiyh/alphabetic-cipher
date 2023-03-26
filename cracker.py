import re
import decoder

def hashWord(word):

    #Translates a word into numbers (starting with 0) where each number uniquely represents a letter in the given word
    #For example: ABC would become 012 - 0 was assigned to 'A', 1 to 'B' and 2 to 'C'
    #Therefore ABCA would become 0120 - since the 'A' at index 0 already exists in the dictionary by the time the program looks at the 'A'
    #at index 3, the second 'A' is assigned the same number as the previous 'A'

    #some more examples:
    #ABCD becomes 0123 --- 0 = A | 1 = B | 2 = C | 3 = D
    
    #ELEPHANT becomes 01023456 --- 0 = E | 1 = L | 0 = E (again) | 2 = P | 3 = H | 4 = A | 5 = N | 6 = T

    #KRUTARTH becomes 01234135 --- 0 = K | 1 = R | 2 = U | 3 = T | 4 = A | 1 = R (again) | 3 = T (again) | 5 = H

    hashed = {}
    out = []
    count = 0

    for char in word:
        if char not in hashed:
            hashed[char] = str(count)
            count += 1
        out.append(hashed[char])
    return ''.join(out)
    
#This is a helper function to create a python translation mapping table from a dictionary of key-value pairs in order to translate the encrypted wordfr5.

def makeTranslations(translations):
    fromStr = ''
    toStr = ''

    for key in translations:
        fromStr += key
        toStr += translations[key]

    return str.maketrans(fromStr, toStr)
    
#Initializes a dictionary where the keys are the hashedWords from the above method and the values are lists containing words that can match that key
#The words in this dictionary come from 'words.txt' which contains a list of 40000+ words
#For example if the key is 012 its values would be words like: cat, bat, hat, mat, pat, rat etc.
#In python dictionary notation, it looks like: {'012' : ['bat', 'cat', 'hat', 'mat', 'pat', 'let']}

#This is eventually used to match the ciphertext hashes to potential words
       
def load_hashed_words():
    wordsList = open('words2.txt').read().splitlines()
    hashDict = {}

    for word in wordsList:
        hashedWord = hashWord(word)

        if hashedWord not in hashDict:
            hashDict[hashedWord] = [word]
            continue
        hashDict[hashedWord].append(word)
    return hashDict
        
def load_ciphertext():
	text = open('ciphertext.txt').read().strip()
	text = re.sub(r'[^\w ]+', '', text)
	return text
    
def solve(remainWords, currTrans, unkWordCount, hashDict):

    trans = makeTranslations(currTrans)

    if len(remainWords) == 0:
        return currTrans

    cipherWord = remainWords[0]

    testWord = cipherWord.translate(trans)
      
    hashedCipherWord = hashWord(testWord)
    potentialWords = []

    #if the hash matches any key in the hashDict then we check a list of all words with that key, otherwise empty list
    if (hashedCipherWord in hashDict):
        for word in (hashDict[hashedCipherWord]):
            valid = True

            for i in range(len(word)):
                if (testWord[i].islower() or testWord[i] == "'" or word[i] == "'") and (testWord[i] != word[i]):
                    valid = False
                    break
            if valid:
                potentialWords.append(word)

    potential = potentialWords

    for p in potential:
        newTrans = dict(currTrans)
        translatedPlainChars = set(currTrans.values())
        badTrans = False

        for i in range(len(p)):
            cipherChar = cipherWord[i]
            plainChar = p[i]

            if ((cipherChar not in currTrans) and (plainChar in translatedPlainChars)):
                badTrans = True
                break
            newTrans[cipherWord[i]] = p[i]

        if badTrans:
            continue

        res = solve(remainWords[1:], newTrans, unkWordCount, hashDict)

        if res:
            return res

    return None

def main():
    ciphertext = load_ciphertext().upper()
    words = sorted(ciphertext.split(), key=lambda word: -len(word))
    hashDict = load_hashed_words()
    solution = solve(words, {}, 0, hashDict)
    
    if not solution:
    	print("Failed to find a solution")
    else:
        plaintext = ciphertext.translate(makeTranslations(solution))
        decoder.print_solution(ciphertext, plaintext, solution)

if (__name__ == "__main__"):
	main()
