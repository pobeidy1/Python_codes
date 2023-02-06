import pickle

def save_vars_pickle (filename, vars_list):
    open_file = open (f' {filename} .pckl', "wb")
    pickle.dump(vars_list, open_file)
    open_file.close()
    
def upload_vars_pickle(filename):
    # open a file, where you stored the pickled data
    file = open(f' {filename} .pckl', 'rb')
    
    # load information from the file
    data = pickle.load(file)
    
    # close the file
    file.close()
    
