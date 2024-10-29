#import the necessary module
import os
import argparse
from hashlib import md5
import filecmp

#Error Message
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."


def valid_path(path):
    # validate file path
    return os.path.exists(path)

def show(args):
    # get path to directory
    dir_path = args.show[0]
     
    # validate path
    if not valid_path(dir_path):
        print("Error: No such directory found.")
        exit()
 
    # get all the files in directory
    for root, dirs, files in os.walk(dir_path):
         for file in files:
                print(os.path.join(root, file))

def find_potential_dupes(args):
    # get the path directory
    dir_path = args.potential_dups[0]
    # validate the path
    if not valid_path(dir_path):
        print("Error: No such directory found.")
        exit()

    # recording the file and size
    file_hashes = {}
    duplicate_hashes = set()

    # check all the files in the directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            path = os.path.join(root, file)
            this_path = os.path.join(root, file)
            with open(path ,'rb') as f:
                file_hash = md5(f.read()).hexdigest()
            
            if file_hash in file_hashes.keys():
                file_hashes[file_hash].append(os.path.join(root,file))
                duplicate_hashes.add(file_hash)
            else:
                file_hashes[file_hash] = [os.path.join(root,file)]
    
    # printing the potential duplicates
    dup_list = []
    for file_hsh in enumerate(duplicate_hashes):
        p_duplicate_files = set()
        print('Potential duplicates', file_hsh[0], ': hash = ', file_hsh[1])
        for file in file_hashes[file_hsh[1]]:
            p_duplicate_files.add(file)
            print(file , end = ", ")
        print('\n')
        dup_list.append(p_duplicate_files)
    
    
    confirmDuplicates(dup_list)


def confirmDuplicates(file_paths):
    """
    @param: file_paths -> list of sets of paths to potentially duplicate
    files that are to be further compared.

    compares files on the byte level and returns the list of files that are 
    duplicates
    """
    for file_set in file_paths:
        # form pairs for comparison
        file_list = list(file_set)
        pairs = []
        for i in range(len(file_list)):
            for j in range(i+1, len(file_list)):
                pairs.append((file_list[i], file_list[j]))

        #compare each of the pairs at the byte level using cmp
        for pair in pairs:
            if filecmp.cmp(pair[0], pair[1]):
                print('Absolute duplicates: ', pair[0], "    ", pair[1] )
            








def main():
    # creating the parser object
    parser = argparse.ArgumentParser(description = "A file deduplication tool!")

    # defining arguments for parser object
    parser.add_argument("-s", "--show", type = str, nargs = 1,
        metavar = "directory", default = None,
        help = "Recursively displays all the files in the specified folders and subfolder\
        Type '.' for current directory.")
    
    parser.add_argument("-p", "--potential_dups", type = str, nargs = 1,
        metavar= "directory", default = None,
        help = "Recursively checks the folder for potentially duplicate files\
        Type '.' for the current direectory.")
    
    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.show != None:
        show(args)
    if args.potential_dups != None:
        find_potential_dupes(args)


if __name__ == "__main__":
    # calling the main function
    main()