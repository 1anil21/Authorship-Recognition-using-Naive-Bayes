import sys, os, operator, json

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
                
                # Make case-folding to word
                word = str.lower(word)

                # Count Tags and Words
                countTag(tag, prev_tag, tags, tag_trans)
                countWord(word, tag, words)
                prev_tag = tag
                
        else:
            # Before starting a new sentence previous tag is cleared
            prev_tag = ""
    
    # Convert tag counts to probabilities
    calculateTagTransitionProbs()
    
    # Calculate total tag count
    total_tags = sum(tags.values())
    
    # Caluclate most probable tag for unknown words
    calculateUnknown(total_tags)
    
    # Convert word counts to probabilities
    calculateWordProbs()
    
    #print (tag_trans)
    #print (tags)
    #print (words)
    #print (unknown_probs)

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
# Divide this count by the occurence of this tag
# Then multiple the result with percentage of tag among all tags
def calculateUnknown(total_tags):

    # For each tag
    for tag in tags:
        count = 0
        
        # For each word assigned to current tag
        # Count the words that have 1 occurence for each tag
        for word in words[tag]:
            if (words[tag][word] == 1):
                count += 1
        
        tag_percent = tags[tag] / total_tags
        
        # Prior probability and smoothing with tag_percent
        unknown_probs[tag] = (count / tags[tag] * tag_percent + tag_percent) / total_tags

# Calculate Word Likelihood Probabilities
def calculateWordProbs():
    
    for tag in words:
        for word in words[tag]:
            words[tag][word] = words[tag][word] / tags[tag]
    
def exportInfo():
    
    with open('words.txt', 'w') as outfile:
        json.dump(words, outfile)
    
    print ("words.txt is created for word probabilities")
        
    with open('tag_transition.txt', 'w') as outfile:
        json.dump(tag_trans, outfile)
    
    print ("tag_transition.txt is created for tag transition probabilities")
        
    with open('unknown_words.txt', 'w') as outfile:
        json.dump(unknown_probs, outfile)
        
    print ("unknown_words.txt is created for unknown word probabilities")
    
    with open('tag_type.txt', 'w') as outfile:
        json.dump(tag_type, outfile)
        
    print ("tag_type.txt is created for tag type")

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
    
    
    