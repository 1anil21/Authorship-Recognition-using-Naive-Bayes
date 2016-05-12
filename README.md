# Authorship-Recognition-using-Naive-Bayes
Authorship Recognition using Naive Bayes

This program learns authors from raw data and predicts authors of documents. It is implemented in Python 3 language. Thereore, it must be run on Python 3.
Moreover, snowball turkish stemming library is used. In order to deactive it please change the constant value in top of identify_author.py.

In order to generate training and test files from raw files, first run build.py with python using directory arguments:

    python build.py -data RAW_TEXT_DIRECTORY -training TRAINING_DATA_DIRECTORY -test TEST_DATA_DIRECTORY

For example:

    python build.py -data C:/69yazar/raw_texts -training C:/69yazar/training -test C:/69yazar/test

In order to run recognition system, run identify_author.py with python using directory arguments:

    python identify_author.py -training TRAINING_DATA_DIRECTORY -test TEST_DATA

For example:

    python identify_author.py -training C:/69yazar/training -test C:/69yazar/test
