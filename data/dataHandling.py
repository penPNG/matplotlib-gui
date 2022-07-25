import re
import pandas as pd

class DataHandling():

    def __init__(self):
        pass    # Felt like this needed to be here, it did not

    def createDict(self, f, tabs):
        if(tabs):
            f = f.replace('\n', '\t')   # So we can keep track of every item
            f = re.split(r'\t', f)      # and then put them in a list
            counter = 0
            data = {}
            for i in f:
                if counter > 2:
                    data[keys[counter%3]].append(i)   # Somehow I got this right on the first try, thank god. Modulo 3 so we can just keep counting the counter
                    counter += 1
                    continue
                data[i] = []    # When formatted correctly, should create some keys in the dictionary
                if counter == 2:  # number of keys -1
                    keys = list(data.keys())    # Create a list of keys
                    print(keys) # Debugging
                counter += 1
        if(not tabs):
            f = f.replace('\n', ' ')   # So we can keep track of every item
            f = re.split(r' ', f)      # and then put them in a list
            counter = 0
            data = {}
            for i in f:
                if counter > 2:
                    data[keys[counter%3]].append(i)   # Somehow I got this right on the first try, thank god. Modulo 3 so we can just keep counting the counter
                    counter += 1
                    continue
                data[i] = []    # When formatted correctly, should create some keys in the dictionary
                if counter == 2:  # number of keys -1
                    keys = list(data.keys())    # Create a list of keys
                    print(keys) # Debugging
                counter += 1


        print(data)
        return data
    
    def organizeInSet(self, d):
        dataSet = pd.DataFrame(d)
        #print(dataSet)
        return dataSet


# Not to be run on it's own, btw
#-------------------------------
if __name__ == '__main__':
    handle = DataHandling("./testfile.txt")
    th, qq, to = handle.putInLists()
    print(th, qq, to)