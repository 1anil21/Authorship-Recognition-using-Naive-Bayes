import sys, os, operator, csv, json

FILE_ENCODING = "utf-8"

# Tag transition probabilities
tag_trans = dict()

# Tag counts
tags = dict()

# All word probabilities
# words[tag][word] means a word's probability for specific tag
words = dict()

# Probabilities for unknown words are stored
unknown_probs = dict()

# The tag is most posibble for unknown words
unknown_tag = ""

# This function trains every word and tag
# Calculate all word and transition probabilities
def train(file_path):

    # Open file with given encoding
    with open(file_path, encoding=FILE_ENCODING) as file:
        lines = file.readlines()
        
    prev_tag = "" # previous tag
    
    for line in lines:
        
        # Skip empty lines
        if (line != "\n"):
            
            # Get fields of the line
            # 1: word, 2: lemma, 3:cpostag, 4:postag
            fields = line.split("\t")
            
            word = fields[1]
            if (tag_type == 1): # CPOSTAG
                tag = fields[3]
            else: # POSTAG
                tag = fields[4]
                                
            # Skip underscored lines
            if (word != "_"):

                # Count Tags and Words
                countTag(tag, prev_tag, tags, tag_trans)
                countWord(word, tag, words)
                prev_tag = tag
                
        else:
            # Before starting a new sentence previous tag is cleared
            prev_tag = ""
    
    calculateTagTransitionProbs()
    
    # Calculate total tag count
    total_tags = sum(tags.values())
    
    # Caluclate most probable tag for unknown words
    calculateUnknown(total_tags)
        
    #print (tag_trans)
    print (tags)
    #print (words)
    #print (unknown_tag)

def countTag(current, previous, tags, tag_trans):
    
    # Count tags
    if (current in tags):
        tags[current] = tags[current] + 1
    else:
        tags[current] = 1
    
    # Tag transition calculation
    if (previous != ""):
        
        if (previous in tag_trans):
            if (current in tag_trans[previous]):
                tag_trans[previous][current] = tag_trans[previous][current] + 1
            else:
                tag_trans[previous][current] = 1
        else:
            tag_trans[previous] = dict()    
            tag_trans[previous][current] = 1
            
def countWord(word, tag, words):
    
    if (tag in words):
        if (word in words[tag]):
            words[tag][word] = words[tag][word] + 1
        else:
            words[tag][word] = 1
    else:
        words[tag] = dict()    
        words[tag][word] = 1

# Find tag transition probabilities from counts 
def calculateTagTransitionProbs():
    
    for tag in tag_trans:
        for tag2 in tag_trans[tag]:
            tag_trans[tag][tag2] = tag_trans[tag][tag2] / tags[tag]

# Find unknown words' probabilities for each tag
# Count the words that have 1 occurence for each tag
# Divide this count by the count of distinct words on this tag
# Then multiple the result with percentage of tag among all tags
def calculateUnknown(total_tags):
    global unknown_tag

    # For each tag
    for tag in tags:
        count = 0
        
        # For each word assigned to current tag
        # Count the words that have 1 occurence for each tag
        for word in words[tag]:
            if (words[tag][word] == 1):
                count += 1
        
        tag_percent = tags[tag] / total_tags
        unknown_probs[tag] = count / len(words[tag]) * tag_percent
        
    # Find most probable tag
    unknown_tag = max(unknown_probs.keys(), key=(lambda k: unknown_probs[k]))
    
def exportInfo():
    
    with open('words.txt', 'w') as outfile:
        json.dump(words, outfile)
        
    with open('tag_transition.txt', 'w') as outfile:
        json.dump(tag_trans, outfile)
        
    with open('unknown_words_tag.txt', 'w') as outfile:
        json.dump(unknown_tag, outfile)

if __name__ == "__main__":

    if (len(sys.argv) < 3):
        print("Please enter all arguments")
        print("Usage: python train_hmm_tagger.py <training_filename> --[cpostag|postag]")
        exit()
        
    training_filename = sys.argv[1]
    tag_type = sys.argv[2]
    
    if (tag_type != "--cpostag" and tag_type != "--postag"):
        print("Please enter valid tagset: --cpostag or --postag")
        exit()
        
    if (tag_type == "--cpostag"):
        tag_type = 1
    else:
        tag_type = 2
    
    train(training_filename)
    exportInfo()
    
    