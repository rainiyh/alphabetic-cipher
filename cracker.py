import argparse
import re


def hashWord(word):

    #Translates a word into numbers (starting with 0) where each number uniquely represents a letter in the given word
    #For example: ABC would become 012 - 0 was assigned to 'A', 1 to 'B' and 2 to 'C'
    #Therefore ABCA would become 0120 - since the 'A' at index 0 already exists in the dictionary by the time the program looks at the 'A'
    #at index 3, the second 'A' is assigned the same number as the previous 'A'

    #some more examples:
    #ABCD becomes 0123 --- 0 = A | 1 = B | 2 = C | 3 = D
    
    #ELEPHANT becomes 01023456 --- 0 = E | 1 = L | 0 = E (again) | 2 = P | 3 = H | 4 = A | 5 = N | 6 = T

    #KRUTARTH becomes 01234135 --- 0 = K | 1 = R | 2 = U | 3 = T | 4 = A | 1 = R (again) | 3 = T (again) | 5 = H

    exists = {}
    out = []
    count = 0

    for ch in word:
        if ch not in exists:
            exists[ch] = str(count)
            count += 1
        out.append(exists[ch])
    return ''.join(out)


class wordDict(object):

    #Initializes a dictionary where the keys are the hashedWords from the above method and the values are lists containing words that can match that key
    #The words in this dictionary come from 'words.txt' which contains a list of 40000+ words

    #For example if the key is 012 its values would be words like: cat, bat, hat, mat, pat, rat etc.
    #In python dictionary notation, it looks like: {'012' : ['bat', 'cat', 'hat', 'mat', 'pat']}

    #This is eventually used to match the ciphertext hashes to potential words

    def __init__(self):

        wordsList = open('words2.txt').read().splitlines()

        self.hashDict = {}

        for word in wordsList:
            hashedWord = hashWord(word)

            if hashedWord not in self.hashDict:
                self.hashDict[hashedWord] = [word]
            else:
                self.hashDict[hashedWord].append(word)

    def findPotentialWords(self, cipherWord):

        hashedCipherWord = hashWord(cipherWord)

        matches = self.hashDict.get(hashedCipherWord) or [] #if the hash matches any key in the hashDict then matches is a list of all words with that key, otherwise empty list

        potentialWords = []

        for word in matches:
            invalid = False

            for i in range(0, len(word)):
                if (cipherWord[i].islower() or cipherWord[i] == "'" or word[i] == "'") and (cipherWord[i] != word[i]):
                    invalid = True
                    break
                if not invalid:
                    potentialWords.append(word)

        return potentialWords

class Solver(object):

    def __init__(self, ciphertext, verbose=False):

        self.wordsFile = wordDict()
        self.translation = {}
        self.ciphertext = ciphertext.upper()
        self.verbose = verbose

    def solve(self):

        words = re.sub(r'[^\w ]+', '', self.ciphertext).split()
        words.sort(key=lambda word: -len(word))

        for maxUnkWordCount in range(0, max(3, len(words) // 10)):

            solution = self.recursiveSolver(words, {}, 0, maxUnkWordCount)

            if solution:
                self.translation = solution
                break

    def recursiveSolver(self, remainWords, currTrans, unkWordCount, maxUnkWordCount):

        trans = self.makeTranslations(currTrans)

        if self.verbose:
            print(self.ciphertext.translate(trans))

        if len(remainWords) == 0:
            return currTrans
        
        if unkWordCount > maxUnkWordCount:
            return None

        cipherWord = remainWords[0]

        potential = self.wordsFile.findPotentialWords(cipherWord.translate(trans))

        for p in potential:
            newTrans = dict(currTrans)
            translatedPlainChars = set(currTrans.values())
            badTrans = False

            for i in range(0, len(p)):
                cipherChar = cipherWord[i]
                plainChar = p[i]

                if (cipherChar not in currTrans and plainChar in translatedPlainChars):
                    badTrans = True
                    break
                
                newTrans[cipherWord[i]] = p[i]

            if badTrans:
                continue

            res = self.recursiveSolver(remainWords[1:], newTrans, unkWordCount, maxUnkWordCount)

            if res:
                return res

            skipWordSol = self.recursiveSolver(remainWords[1:], currTrans, unkWordCount + 1, maxUnkWordCount)

            if skipWordSol:
                return skipWordSol

            return None


    @staticmethod
    def makeTranslations(translations):

        fromStr = ''
        toStr = ''

        for key in translations:
            fromStr += key
            toStr += translations[key]

        return str.maketrans(fromStr, toStr)

    def printSol(self):

        if not self.translation:
            print("Could not translate")
            return
        
        plaintext = self.ciphertext.translate(Solver.makeTranslations(self.translation))

        print('Ciphertext:')
        print(self.ciphertext)
        print("Plaintext:")
        print(plaintext)




def main():

    ciphertext = open('ciphertext.txt').read().strip()

    solver = Solver(ciphertext)

    solver.solve()

    solver.printSol()


main()


# c = makeTrans2(b)

# print(c)
