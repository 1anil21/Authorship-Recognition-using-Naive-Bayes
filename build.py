import argparse, os, random, shutil
from shutil import copyfile

# Randomly 60% of dataset will be training set
TRAINING_RATE = 3/5;

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-data', '--data-set', type=str, help='Directory of dataset includes directory of authors', dest='dataset')
    parser.add_argument('-training', '--training-set', type=str, help='Directory of training set will be generated', dest='training')
    parser.add_argument('-test', '--test-set', type=str , help='Directory of test set will be generated', dest='test')
    opts = parser.parse_args()

    if (opts.dataset == None or opts.training == None or opts.test == None):
        print ("Please enter all arguments")
        parser.print_usage()
        exit()
    
    # Create training and test directories
    # If they exist remove first
    if (os.path.isdir(opts.training)):
        shutil.rmtree(opts.training)
    if (os.path.isdir(opts.test)):
        shutil.rmtree(opts.test)
    
    os.mkdir(opts.training)
    os.mkdir(opts.test)

    # Get all directories in given dataset directory
    for root, dirs, files in os.walk(opts.dataset):

        # For all directories
        for dirname in dirs:
            
            # Create directories in training and test folders
            os.mkdir(opts.training+"/"+dirname)
            os.mkdir(opts.test+"/"+dirname)
            
            # Get filelist and total file count from directory
            files = [filename for filename in os.listdir(opts.dataset+"/"+dirname) if filename.endswith(".txt") ]
            file_count = len(files)

            # Get file_count * TRAINING_RATE samples to decide indexes of training files
            # Get indexes of test files by substracting indexes of training files from all indexes
            training_file_indexes = list(random.sample(range(file_count), int(file_count*TRAINING_RATE)))
            test_file_indexes = list(set(range(file_count)) - set(training_file_indexes))
            
            # For all files in directory
            for i in range(file_count):
                
                # If training file copy to corresponding training folder
                # Else copy to corresponding test folder
                if i in training_file_indexes:
                    copyfile (opts.dataset+"/"+dirname+"/"+files[i], opts.training+"/"+dirname+"/"+files[i])
                else:
                    copyfile (opts.dataset+"/"+dirname+"/"+files[i], opts.test+"/"+dirname+"/"+files[i])
                    
            print ("Pre-processing is done for directory " + dirname)
