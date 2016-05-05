import sys, os, operator, json

FILE_ENCODING = "utf-8"

output_tags = []
test_gold_tags = []
tags = dict()
confusion_matrix = []

def readFiles(output_path, test_gold_path):

    # Open output file with given encoding
    with open(output_path, encoding=FILE_ENCODING) as file:
        lines = file.readlines()

    for line in lines:

        # If line has a word
        if (line != "\n"):

            # Get fields of the line
            # 1: word, 2: lemma
            fields = line.split("|")
            
            # Add tag to list
            output_tags.append(fields[1].rstrip())
            
            
    # Open test gold file with given encoding
    with open(test_gold_path, encoding=FILE_ENCODING) as file2:
        lines = file2.readlines()

    for line in lines:
    
        # If line has a word
        if (line != "\n"):
            
            # Get fields of the line
            # 1: word, 2: lemma
            fields = line.split("\t")
            
            word = fields[1]
            
            # Skip underscored lines
            if (word != "_"): 
                test_gold_tags.append(fields[2+tag_type])
            
def evaluateFiles():
    
    if len(output_tags) != len(test_gold_tags):
        print ("Word counts are not equal for both file")
        exit()
    
    correct_tags = 0
    total_tags = 0
    
    for i in range(0, len(output_tags)):
        if (output_tags[i] == test_gold_tags[i]):
            correct_tags += 1
        else: #Error counting
            tagged_index = tags[output_tags[i]]
            real_tag_index = tags[test_gold_tags[i]]
            
            confusion_matrix[real_tag_index][tagged_index] += 1
            
        total_tags += 1
    
    print ("Correct tags: " + str(correct_tags))
    print ("Total tags: " + str(total_tags))
    print ("Accuracy: " + str(correct_tags/total_tags * 100) + "%")

def printConfusionMatrix():
    
    print ()
    print ("Confusion Matrix: (Rows: Real Tags, Columns: Tagged Tags)")
    print ()
    
    row_format ="{:^11}" * (len(tags) + 1)
    print (row_format.format("", *tags))
    
    for tag, val in zip(tags, confusion_matrix):
        print (row_format.format(tag, *val))
    
if __name__ == "__main__":

    if (len(sys.argv) < 3):
        print("Please enter all arguments")
        print("Usage: python hmm_tagger.py <output_filename> <test_gold_filename>")
        exit()
    
    output_filename = sys.argv[1]
    test_gold_filename = sys.argv[2]
    
    # Get tag type of trained file
    tag_type_file = open("tag_type.txt","r")
    tag_type = json.load(tag_type_file)
    
    # Get tags
    tag_transition_file = open("tag_transition.txt","r")
    tag_trans = json.load(tag_transition_file)
    
    # Enumerate tags
    i = 0
    for tag in tag_trans:
        tags[tag] = i
        i += 1
        
    tags_size = len(tags)

    # Create confusion matrix
    confusion_matrix = [[0 for x in range(tags_size)] for y in range(tags_size)] 
    
    readFiles(output_filename, test_gold_filename)
    
    evaluateFiles()
    
    printConfusionMatrix()
    