from __future__ import unicode_literals
import argparse, os, re, sys, operator, math
import snowballstemmer

FILE_ENCODING = "windows-1254"
SMOOTHING_CONST = 0.1
STEMMING = True

# Create stemmer
stemmer = snowballstemmer.stemmer("turkish")

# prior_prob is a dictionary contains prior probabilities of authors
prior_prob = dict()

# word_prob is a dictionary contains dictionaries of authors which include word probabilities
word_prob = dict()

# Dictionary includes the number of words in the all training data of each author
total_words = dict()

# total_docs is the number of documents in training set
total_docs = 0

# authors is the list contains all author names
authors = []

# unknown word probabilities for each author
unknown_prob = dict()

# total vocabulary set
vocabulary = []

# Results dictionary keys are authors of files
results = dict()

# True positives for each author
tps = dict()

# False positives for each author
fps = dict()

# False negatives for each author
fns = dict()

# Recalls for each author
recalls = dict()

# Precisions for each author
precisions = dict()

# F-Scores for each author
fscores = dict()

# Micro-averaged results for each author
microavg = dict()

# This function returns a list of tokens for given file
def tokenize(filedir):

    # Open file with given encoding
    with open(filedir, encoding=FILE_ENCODING) as file:
        lines = file.readlines()

    # join all lines in file to get file content
    content = "\n".join(lines).strip()

    # Get tokens by using turkish word pattern which also excludes numbers
    tokens = re.findall(r'\b([A-Za-zıİöÖüÜğĞşŞçÇ]+)\b', content)

    return tokens

# This function makes case-folding for a list of tokens
def preprocess(tokens):
    if (STEMMING):
        return [stemmer.stemWord(token.lower()) for token in tokens]
    else:
        return [token.lower() for token in tokens]
    
# This function counts tokens and creates a dictionary for them with their occurences
def countTokens(tokens):

    dictionary = dict([ (i, tokens.count(i)) for i in set(tokens)])

    return dictionary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-training', '--training-set', type=str, help='Directory of training set will be learned', dest='training')
    parser.add_argument('-test', '--test-set', type=str , help='Directory of test set will be tested', dest='test')
    opts = parser.parse_args()

    if (opts.training == None or opts.test == None):
        print ("Please enter all arguments")
        parser.print_usage()
        exit()

    # LEARNING PART

    print ("\nLEARNING PART\n")

    # Get all directories in given training set directory
    for root, dirs, files in os.walk(opts.training):

        # For all directories/authors
        for dirname in dirs:

            # Add author to authors list
            authors.append(dirname)

            # Get all filenames of current author in given training directory
            files = [filename for filename in os.listdir(opts.training+"/"+dirname) if filename.endswith(".txt") ]

            # Assign each author with its count of documents
            prior_prob[dirname] = len(files)

            # Count total number of documents
            total_docs += len(files)

            tokens = []

            # Get all tokens from training documents of current author
            # Append them into common tokens list
            for file in files:
                tokens.extend(tokenize(opts.training+"/"+dirname+"/"+file))

            # Store total words of author
            total_words[dirname] = len(tokens)

            # Make preprocessing for all words of author
            tokens = preprocess(tokens)

            # Add unique words to vocabulary
            vocabulary.extend(list(set(tokens)))

            # Counts of words for all training documents of author
            word_counts = countTokens(tokens)

            # Attach word counts of current author to word_prob dictionary
            word_prob[dirname] = word_counts

            print(dirname + " is processed!")
            
    # Calculate prior probabilities by dividing counts of documents by total document count
    # Use underflow prevention by taking logarithm of probabilities
    for author, count in prior_prob.items():
        prior_prob[author] = math.log10( count / total_docs )

    # Calculate Vocabulary Size
    vocabulary_size = len(set(vocabulary))

    # For each author, calculate word probabilities for author by dividing word count by total word count
    # Use Laplace smoothing by adding 1 to numerator, and adding vocabulary size to denominator
    # Use underflow prevention by taking logarithm of probabilities
    for author in authors:
        for word in word_prob[author]:
            word_prob[author][word] = math.log10( (word_prob[author][word] + SMOOTHING_CONST) / (total_words[author] + vocabulary_size ) )

    # For each author, calculate unknown word probabilities
    for author in authors:
        unknown_prob[author] = math.log10 ( (0 + SMOOTHING_CONST) / (total_words[author] + vocabulary_size) )

    # TESTING PART

    print ("\nTESTING PART\n")

    # Get all directories in given test set directory
    for root, dirs, files in os.walk(opts.test):

        # For all directories/authors
        for dirname in dirs:
            
            # Store results of author in this list
            author_results = []

            # Get all filenames of current author in given test directory
            files = [filename for filename in os.listdir(opts.test+"/"+dirname) if filename.endswith(".txt") ]

            words = []

            # For each document
            for file in files:

                # Get all words from test document
                words = tokenize(opts.test+"/"+dirname+"/"+file)
                
                # Make preprocessing for all words of author
                words = preprocess(words)

                # Probabilities that current document belongs to an author
                result_prob = dict()

                # For each author
                # Calculate probability that document belongs to that author and put result_prob dictionary
                for author in authors:

                    # Probability for current author set to 0
                    result_prob[author] = 0

                    # First add prior probability
                    result_prob[author] += prior_prob[author]

                    # For each word in document
                    for word in words:
                        # If word exists in training set then add probability of word
                        if (word in word_prob[author]):
                            result_prob[author] += word_prob[author][word]
                        # If word is unknown then calculate probability with Laplace smooting
                        else:
                            result_prob[author] += unknown_prob[author]

                # Get the author has maximum probability as test result
                result = max(result_prob.items(), key=operator.itemgetter(1))[0]

                author_results.append(result)

            # Store results of dirname (author)
            results[dirname] = author_results
            
            print (dirname + " is tested!")

    # Calculate true-positives, false-positives and false negatives for each author
    for author in authors:
        
        tp = 0
        fp = 0
        fn = 0
        
        # Check author's results
        for result in results[author]:
            if (result == author):
                tp = tp + 1
            else:
                fn = fn + 1
        
        # Check other author's results for current author
        for author2 in authors:
            if (author2 != author):
                for result in results[author2]:
                    if (result == author):
                        fp = fp + 1

        tps[author] = tp
        fps[author] = fp
        fns[author] = fn
    
    # Calculate precision, recall and f-score for each author
    for author in authors:
        if (tps[author] + fps[author] == 0):
            precisions[author] = 0
        else:
            precisions[author] = tps[author] / (tps[author] + fps[author])
        
        if (tps[author] + fns[author] == 0):
            recalls[author] = 0
        else:
            recalls[author] = tps[author] / (tps[author] + fns[author])
        
        if (precisions[author] + recalls[author] == 0):
            precisions[author] = 0
        else:
            fscores[author] = (2 * precisions[author] * recalls[author]) / (precisions[author] + recalls[author])
    
    # Calculate macro-averaged precision
    macro_avg_precision = 0
    for author, precision in precisions.items():
        macro_avg_precision += precision
    macro_avg_precision = macro_avg_precision / float(len(precisions))
    
    # Calculate macro-averaged recall
    macro_avg_recall = 0
    for author, recall in recalls.items():
        macro_avg_recall += recall
    macro_avg_recall = macro_avg_recall / float(len(recalls))
    
    # Calculate macro-averaged fscores
    macro_avg_fscore = 2 * macro_avg_precision * macro_avg_recall / (macro_avg_precision + macro_avg_recall)
    
    # Calculate total true positives, false positives, and false negatives
    total_tps = sum(tps.values())
    total_fps = sum(fps.values())
    total_fns = sum(fns.values())
    
    # Calculate micro-averaged precision
    micro_avg_precision = total_tps / (total_tps + total_fps)
    
    # Calculate micro-averaged recall
    micro_avg_recall = total_tps / (total_tps + total_fns)
    
    # Calculate micro-averaged fscores
    micro_avg_fscore = 2 * micro_avg_precision * micro_avg_recall / (micro_avg_precision + micro_avg_recall)
        
    # Print Results
    print ()
    print ("Macro-averaged precision:" + str(macro_avg_precision))
    print ("Macro-averaged recall:" + str(macro_avg_recall))
    print ("Macro-averaged f-score:" + str(macro_avg_fscore))
        
    print ("Micro-averaged precision:" + str(micro_avg_precision))
    print ("Micro-averaged recall:" + str(micro_avg_recall))
    print ("Micro-averaged f-score:" + str(micro_avg_fscore))
