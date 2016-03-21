# Authorship-Recognition-using-Naive-Bayes
Authorship Recognition using Naive Bayes

This program learns authors from raw data and predicts authors of documents. It is implemented in Python language.

In order to generate training and test files from raw files, first run build.py with python using directory arguments:
python build.py -data RAW_TEXT_DIRECTORY -training TRAINING_DATA_DIRECTORY -test TEST_DATA DIRECTORY

For example:
python build.py -data C:/authorship_recognition/raw_texts -training C:/authorship_recognition/training -test C:/authorship_recognition/test

In order to run recognition system, run identify_author.py with python using directory arguments:
python identify_author.py -training TRAINING_DATA_DIRECTORY -test TEST_DATA

For example:
python identify_author.py -training C:/authorship_recognition/training -test C:/authorship_recognition/test
