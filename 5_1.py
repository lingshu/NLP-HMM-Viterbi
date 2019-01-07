#! /usr/bin/python
import os
from math import log
from collections import defaultdict

def get_bigram_trigram(input_file = "ner_rare.counts"):
    bigram = defaultdict(float)
    trigram = defaultdict(float)

    with open(input_file) as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split()
                if fields[1] == "2-GRAM":
                    bigram[(fields[2], fields[3])] = float(fields[0])
                if fields[1] == "3-GRAM":
                    trigram[(fields[2], fields[3], fields[4])] = float(fields[0])
            l = f.readline()
    return bigram, trigram

def get_trigram_prob():
    trigram_prob = defaultdict(float)
    for key, value in trigram.items():
        trigram_prob[key] = log(value) - log(bigram[(key[0], key[1])])
    return trigram_prob

def get_output_file(intput_file = "trigrams.txt", output_file = "5_1.txt"):
    with open(intput_file, "r") as input, open(output_file, "w") as output:
        l = input.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split()
                output.write("{} {} {} {}\n".format(fields[0], fields[1], fields[2], trigram_prob[(fields[0], fields[1], fields[2])]))
            l = input.readline()


if __name__ == "__main__":
    os.system("python count_freqs.py ner_train_rare.dat > ner_rare.counts")
    bigram, trigram = get_bigram_trigram()
    trigram_prob = get_trigram_prob()
    get_output_file()