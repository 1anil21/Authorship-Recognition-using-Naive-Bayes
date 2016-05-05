import sys, os, operator, json, codecs

FILE_ENCODING = "utf-8"

# Tag transition probabilities
tag_trans = dict()

# All Tags
tags = []

# All word probabilities
# words[tag][word] means a word's probability for specific tag
words = dict()

# Probabilities for unknown words are stored
unknown_probs = dict()

# Output
output = []

def importInfo():
    global words, tag_trans, unknown_probs

    words_file = open("words.txt","r")
    words = json.load(words_file)

    tag_transition_file = open("tag_transition.txt","r")
    tag_trans = json.load(tag_transition_file)

    unknown_tag_file = open("unknown_words.txt","r")
    unknown_probs = json.load(unknown_tag_file)

# Enumerte all tags start with 1
def enumerateTags():

    for tag in tag_trans:
        tags.append(tag)

def testFile(file_path):

    # Open file with given encoding
    with open(file_path, encoding=FILE_ENCODING) as file:
        lines = file.readlines()

    sentence = []
    sentence2 = [] # Sentence that is not applied case-folding

    for line in lines:

        # If line has a word
        if (line != "\n"):

            # Get fields of the line
            # 1: word, 2: lemma
            fields = line.split("\t")

            word = fields[1]

            # Skip underscored lines
            if (word != "_"):
                
                # Add the original word to sentence2 
                sentence2.append(word)

                # Make case-folding to word
                word = str.lower(word)

                # Add the word to current sentence
                sentence.append(word)

        # If a sentence is finished
        else:
             result = doViterbi(sentence)
             
             for i in range(0, len(sentence)):
                 f.write(sentence2[i]+"|"+result[i]+"\n")
            
             f.write("\n")

             sentence.clear()
             sentence2.clear()

def doViterbi(sentence):
    
    result = []

    T = len(sentence) # Number of words in sentence
    N = len(tags) # Number of tags

    # Create viterbi matrix N x T since we do not have start and end transition tags
    viterbi = [[0 for x in range(T)] for y in range(N)]
    backpointer = [[0 for x in range(T)] for y in range(N)]

    # Initialization
    for s in range(0,N): # For each tag (state)
        viterbi[s][0] = getWordProb(sentence[0], tags[s])
        backpointer[s][0] = 0

    # Recursion
    for t in range(1,T): # each word
        for s in range(0,N): # each state

            maxPrevious = 0
            maxPreviousPointer = 0

            # Find max state from previous states
            for r in range(0,N): # each state of previous word
                current = viterbi[r][t-1] * getTagTransitionProb(tags[r], tags[s])
    
                if (current > maxPrevious):
                    maxPrevious = current
                    maxPreviousPointer = r

            viterbi[s][t] = maxPrevious * getWordProb(sentence[t], tags[s])
            backpointer[s][t] = maxPreviousPointer

    # Termination
    lastBackpointer = 0
    lastBackpointerProb = 0
    
    for s in range(0,N): # each state of previous word
        current = viterbi[s][T-1]
        
        if (current > lastBackpointerProb):
            lastBackpointerProb = current
            lastBackpointer = s
    
    result.append(tags[lastBackpointer])

    # Backtrace path by following backpointers
    for t in range(T-1,0,-1):

        lastBackpointer = backpointer[lastBackpointer][t]
        result.append(tags[lastBackpointer])
        
    result = list(reversed(result))

    return result


# Check word probability exists for tag
# If not return unknown word probability for corresponding tag
def getWordProb(word, tag):

    if (word in words[tag]):
        return words[tag][word]
    else:
        return unknown_probs[tag]

def getTagTransitionProb(tag, tag2):

    if tag in tag_trans:
        if tag2 in tag_trans[tag]:
            return tag_trans[tag][tag2]
        else:
            return 0
    else:
        return 0

if __name__ == "__main__":

    if (len(sys.argv) < 3):
        print("Please enter all arguments")
        print("Usage: python hmm_tagger.py <test_blind_filename> <output_filename>")
        exit()

    test_blind_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # Import word and tag transition probabilities from sources
    importInfo()

    # Enumerate all tags into tags dictionary
    enumerateTags()
    
    # Open output file to write results
    f = codecs.open(output_filename, 'w', 'utf-8')

    # Start to test
    testFile(test_blind_filename)
    
    # Close file
    f.close()
    
    print ("Output file is generated!")

