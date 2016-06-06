import numpy as np
import re, os
import networkx as nx
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from nltk.parse import stanford

FILE_ENCODING = "utf8"
TRAINING_SIZE = 3000

os.environ['JAVAHOME'] = "C:/Program Files/Java/jdk1.8.0_40/bin"
os.environ['STANFORD_PARSER'] = '/jars'
os.environ['STANFORD_MODELS'] = '/jars'

parser = stanford.StanfordParser(model_path="/jars/englishPCFG.ser.gz")
dep_parser = stanford.StanfordDependencyParser(model_path="/jars/englishPCFG.ser.gz")

#===========================================================================
# parsed =   parser.raw_parse("Example sentence.")
# dep_parsed = dep_parser.raw_parse("Example sentence.")
#===========================================================================

# Classifier
clf = LinearSVC()

sentences = []
labels = []

def chunks(arr, n):
    for i in range(0, len(arr), n):
        yield arr[i:i+n]

def readData():
    global labels

    # Open labels file with given encoding
    with open("dataset.labels", encoding=FILE_ENCODING) as file:
        lines = file.readlines()
    
    for i in lines:
        labels.append( int(i.strip()))
        
    labels = np.array(labels).astype(np.int)
    
    # Open sentences file with given encoding
    with open("dataset.sentences", encoding=FILE_ENCODING) as file:
        lines = file.readlines()
        
    for sentence in lines:
        sentences.append(sentence.strip())
        
def findBetween():
    
    between = []
    
    for sentence in sentences:
        
        # Substring from PROTX1 to PROTXY2
        lr = re.findall(r'\bPROTX1(.*?)PROTX2\b', sentence)
        
        # Substring from PROTX2 to PROTXY1
        rl = re.findall(r'\bPROTX2(.*?)PROTX1\b', sentence)
        
        if len(lr) > 0:
            between.append (re.findall(r'\b([A-Za-z]+)\b', lr[0]))
        elif len(rl) > 0:
            between.append (re.findall(r'\b([A-Za-z]+)\b', rl[0]))
        else:
            between.append ([])
        
    return between

def makeBetweenSet(between):
    
    betweenSet = set()
    
    for words in between:
        for word in words:
            betweenSet.add(word)
            
    return betweenSet

#===============================================================================
# def readIntKeywords():
#     
#     keywords = []
#     
#     # Open file with given encoding
#     with open("int-keywords.txt", encoding=FILE_ENCODING) as file:
#         lines = file.readlines()
#         
#     for line in lines:
#         keywords.append(line.strip())
#         
#     return keywords
#===============================================================================

def prepareBaselineData(between, betweenSet):
    
    data = []

    # For every sentence take words between two entity
    for betweenWords in between:
        
        sentenceFeatures = []
        
        for feature in betweenSet:
            
            if feature in betweenWords:
                sentenceFeatures.append(1)
            else:
                sentenceFeatures.append(0)
                
        data.append(sentenceFeatures)

    x = np.array(data).astype(np.int)
    
    return x

def findDependencyPaths():
    
    data = []
    chunk_size = 100
    sentence_chunks = chunks(sentences, chunk_size)
    
    i = 0
    for sentence_chunk in sentence_chunks:
    
        dep_parsed = dep_parser.raw_parse_sents(sentence_chunk)
    
        for itemList in dep_parsed:
            
            for item in itemList:
                
                dep = list(item.triples())
            
                G = nx.Graph()
                
                for item in dep:
                    G.add_edge(item[0][0],item[2][0],dep=item[1])
                
                if (G.has_node("PROTX1") and G.has_node("PROTX2") ):
                    
                    path = nx.shortest_path(G, source='PROTX1', target='PROTX2')
                    
                    # Append dependency path to data by removing PROTX1 and PROTX2 words
                    data.append(path[1:-1])
                else:
                    data.append([])
                
        i += chunk_size
        
        print (str(i) + " sentences are parsed.") 

    return data

def makeDependencyPathSet(dependencyPaths):
    
    depPathSets = set()
    
    for words in dependencyPaths:
        for word in words:
            depPathSets.add(word)
            
    return depPathSets

def prepareAdvancedData(dependencyPaths, dependencyPathsSet):
    
    data = []
    
    print (dependencyPathsSet)
    print (dependencyPaths)

    # For every sentence
    for dependencyPath in dependencyPaths:
        
        pathFeatures = []
        
        for feature in dependencyPathsSet:
            
            if feature in dependencyPath:
                pathFeatures.append(1)
            else:
                pathFeatures.append(0)
                
        data.append(pathFeatures)

    x = np.array(data).astype(np.int)
    
    return x

def trainAndTest(data):
    
    # Split Training and Test Data
    trainingData = data[:TRAINING_SIZE]
    trainingLabels = labels[:TRAINING_SIZE]
    
    testData = data[TRAINING_SIZE:]
    trueLabels = labels[TRAINING_SIZE:]

    # Train Classifier
    print (clf.fit(trainingData, trainingLabels))
    predictedLabels = clf.predict(testData)
    
    # Calculate & Print Results
    accuracy = accuracy_score(trueLabels, predictedLabels)
    results = precision_recall_fscore_support(trueLabels, predictedLabels, average="binary")
    precision = results[0]
    recall = results[1]
    fscore = results[2]
    
    print ("accuracy\tprecision\trecall\t\tf1-score")
    print ("%-.2f\t\t%-.2f\t\t%-.2f\t\t%.2f" % (accuracy, precision, recall, fscore) )
    
def baselineSystem():
    
    print ("Reading data...")
    readData()
    
    print ("Finding between words for every sentences...")
    # Between words for every sentences
    between = findBetween()
    
    print ("Finding set of betwee words...")
    # Set of between words
    betweenSet = makeBetweenSet(between)
    
    print ("Preparing baseline data...")
    data = prepareBaselineData(between, betweenSet)
 
    print ("Training and testing data...")
    trainAndTest(data)
    
def advacedSystem():
    
    print ("Reading data...")
    readData()
    
    print ("Finding dependency paths...")
    dependencyPaths = findDependencyPaths()
    
    print ("Creating feature sets from dependency paths...")
    dependencyPathsSet = makeDependencyPathSet(dependencyPaths)
    
    print ("Preparing data with features as dependency paths...")
    data = prepareAdvancedData(dependencyPaths, dependencyPathsSet)
    
    print ("Training and testing data...")
    trainAndTest(data)


if __name__ == "__main__":

    baselineSystem()
    #advacedSystem()
