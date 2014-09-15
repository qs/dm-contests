import re
from os import listdir
from os.path import isfile, join
from collections import defaultdict


class TrainGen:
    def __init__(self):
        self.circles = defaultdict(list)

    def load_real_circles(self):
        train_path = 'Training/'
        onlyfiles = [ join(train_path,f) for f in listdir(train_path) if isfile(join(train_path,f)) ]
        for f in onlyfiles:
            with open(f) as fp:
                user_id = re.search(r"\/([0-9]+)\.", f).group(1)
                circles = [s.split(' ') for s in re.findall(r": ([0-9 ]+)", fp.read())]
                self.circles[user_id] = circles

    def train_user_list(self):
        print self.circles.keys()
        return self.circles.keys()

    def write_results(self):
        with open('result_real.csv', 'w') as fp:
            fp.write("UserId,Predicted\n")
            for user_id, circles in self.circles.iteritems():
                row = "%s," % user_id
                row += ';'.join([' '.join(c) for c in circles if c]) + '\n'
                fp.write(row)

if __name__ == "__main__":
    tg = TrainGen()
    tg.load_real_circles()
    tg.train_user_list()
    #tg.write_results()