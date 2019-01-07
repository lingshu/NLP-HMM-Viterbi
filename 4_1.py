#! /usr/bin/python

import sys
from collections import defaultdict

def make_count_dict(corpus_file="ner_train.dat"):
    count_dict = defaultdict(int)
    with open(corpus_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                word = " ".join(fields[:-1])
                count_dict[word] += 1
            l = f.readline()
    return count_dict

def update_rare(corpus_file="ner_train.dat", threshold = 5):
    update_rare_lines = []
    with open(corpus_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                word = " ".join(fields[:-1])
                ne_tag = fields[-1]
                if count_dict[word] < threshold:
                    update_rare_lines.append(" ".join(["_RARE_", ne_tag]))
                else:
                    update_rare_lines.append(line)
            else:
                update_rare_lines.append(" ")
            l = f.readline()
    return update_rare_lines

def make_rare_output(rare_output_file="ner_train_rare.dat"):
    with open(rare_output_file, 'w') as f:
        f.write('\n'.join(update_rare_lines))

if __name__ == "__main__":
    count_dict = make_count_dict()
    update_rare_lines = update_rare()
    make_rare_output()