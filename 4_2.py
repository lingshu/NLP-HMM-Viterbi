#! /usr/bin/python

import os
from collections import defaultdict
import math

def get_tag_count_dict(input_file="ner_rare.counts"):
    tag_count_dict = defaultdict(int)

    with open(input_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                if fields[1] == "WORDTAG":
                    tag = fields[2]
                    tag_count_dict[tag] += int(fields[0])
            l = f.readline()
    return tag_count_dict

def get_emission_dict(input_file="ner_rare.counts"):
    emission_dict = defaultdict(lambda: defaultdict(lambda: float("-inf")))

    with open(input_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                if fields[1] == "WORDTAG":
                    tag = fields[2]
                    word = " ".join(fields[3:])
                    emission_dict[word][tag] = math.log(float(fields[0])) - math.log(float(tag_count_dict[tag]))
            l = f.readline()
    return emission_dict

def get_maxprobtag_maxprob_dict():
    maxprobtag_maxprob_dict = defaultdict(tuple)

    for word in emission_dict:
        maxprob = float('-inf')
        for tag in emission_dict[word]:
            if emission_dict[word][tag] > maxprob:
                maxprob = emission_dict[word][tag]
                maxprobtag = tag
        maxprobtag_maxprob_dict[word] = (maxprobtag, maxprob)
    return maxprobtag_maxprob_dict

def get_naive_tagger(input_file = "ner_dev.dat", output_file = "4_2.txt"):
    lines = []
    with open(input_file, 'r') as f:
        l = f.readline()
        while l:
            word = l.strip()
            if not word:
                lines.append(' ')
            elif word in maxprobtag_maxprob_dict:
                lines.append("{} {} {}".format(word, maxprobtag_maxprob_dict[word][0], maxprobtag_maxprob_dict[word][1]))
            else:
                lines.append("{} {} {}".format(word, maxprobtag_maxprob_dict['_RARE_'][0], maxprobtag_maxprob_dict['_RARE_'][1]))
            l = f.readline()

    with open(output_file, 'w') as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    os.system("python count_freqs.py ner_train_rare.dat > ner_rare.counts")
    tag_count_dict = get_tag_count_dict()
    emission_dict = get_emission_dict()
    maxprobtag_maxprob_dict = get_maxprobtag_maxprob_dict()
    get_naive_tagger()
