import re
import pandas as pd

class DataHandling():

    def __init__(self):
        pass

    def test(self, f):
        count = 0
        f.replace('\n', "")
        f = re.split(r'\t', f)
        print(f)


if __name__ == '__main__':
    handle = DataHandling("./testfile.txt")
    th, qq, to = handle.putInLists()
    print(th, qq, to)