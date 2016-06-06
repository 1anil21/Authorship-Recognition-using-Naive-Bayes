# HMM POS Tagger
HMM POS Tagger

This program learns part of speech tags of sentences from training data and predicts tags of sentences. 
It is implemented in Python language. Please use Python 3 to run.

In order to train training file first run train_hmm_tagger.py with python using directory arguments:

    python train_hmm_tagger.py <training_filename> --[cpostag|postag]

For example:

    python train_hmm_tagger.py turkish_metu_sabanci_train.conll --cpostag

In order to tag sentences, run hmm_tagger.py with python using directory arguments:

    python hmm_tagger.py <test_blind_filename> <output_filename>

For example:

    python hmm_tagger.py turkish_metu_sabanci_val.conll  output.txt
    
In order to evaluate tagged sentences, run evaluate_hmm_tagger.py with python using directory arguments:

    python evaluate_hmm_tagger.py <output_filename> <test_gold_filename>
    
For example:

    python evaluate_hmm_tagger.py output.txt turkish_metu_sabanci_val.conll  
    
  
