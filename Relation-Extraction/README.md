# Relation Extraction
Relation Extraction

This program identifies whether a sentence describe an interaction between PROTX1 and PROTX2 proteins. In baseline system, classifier learns the words between these two entities in the sentence and uses unigrams of words as features.. In advaned system classifiers learns the dependency path (words) between these two entities in the dependency parse tree and uses unigrams of these words as features.

It is implemented in Python language. Please use Python 3 to run.

In order to execute program:

    python rel_extract.py

Give sentences with "dataset.sentences" and labels with "dataset.labels" files in the same directory with the script.
