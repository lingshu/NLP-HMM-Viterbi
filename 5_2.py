#! /usr/bin/python
from collections import defaultdict
from math import log
import time

def get_bigram_trigram(input_file = "ner_rare.counts"):
    bigram = {}
    trigram = {}

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
                    tag_count_dict[tag] += float(fields[0])
            l = f.readline()
    return tag_count_dict

def get_word_count(input_file = "ner_train_rare.dat"):
    word_count = defaultdict(int)
    with open(input_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                word = " ".join(fields[:-1])
                word_count[word] += 1
            l = f.readline()
    return word_count

def get_available_tags(input_file = "ner_rare.counts"):
    tags = set()
    with open(input_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                if fields[1] == "WORDTAG":
                    tags.add(fields[2])
            l = f.readline()
    return tags

def get_tagset(k):
    if k >= 0:
        return tags
    else:
        return {"*"}

def get_output_file(intermediate, output_file = "5_2.txt"):
    with open(output_file, "w") as f:
        f.write("\n".join(intermediate))
        f.write("\n")

def get_transition_prob():
    q = {}
    bigram, trigram = get_bigram_trigram()
    for (key, value) in trigram.items():
        q[key] = log(value) - log(bigram[(key[0], key[1])])
    return q

def get_emission_prob(input_file="ner_rare.counts"):
    e = defaultdict(lambda: defaultdict(lambda: float("-inf")))
    tag_count_dict = get_tag_count_dict()
    with open(input_file, 'r') as f:
        l = f.readline()
        while l:
            line = l.strip()
            if line:
                fields = line.split(" ")
                if fields[1] == "WORDTAG":
                    tag = fields[2]
                    word = " ".join(fields[3:])
                    e[word][tag] = log(float(fields[0])) - log(tag_count_dict[tag])
            l = f.readline()
    return e

def tagger(input_file = "ner_dev.dat"):
    sentences = []
    with open(input_file, "r") as f:
        l = f.readline()
        sentence = []
        while l:
            word = l.strip()
            if not word:
                sentences.append(sentence)
                sentence = []
            else:
                sentence.append(word)
            l = f.readline()
        if len(sentence) > 0:
            sentences.append(sentence)

    word_count = get_word_count()
    intermediate = []
    for sentence in sentences:
        x = []
        for word in sentence:
            if word not in word_count:
                x.append("_RARE_")
            else:
                x.append(word)
        tag_sequence, prob = run_viterbi_algo(x)
        for i in range(len(x)):
            intermediate.append(" ".join([sentence[i], tag_sequence[i], str(prob[i])]))
        intermediate.append("")

    get_output_file(intermediate)

def run_viterbi_algo(x):
    pi = defaultdict(lambda: float("-inf"))
    bp = defaultdict(str)
    pi[(-1, "*", "*")] = 0
    n = len(x)

    for k in range(n):
        for u in get_tagset(k - 1):
            for v in get_tagset(k):
                max_value = float("-inf")
                arg_max = ""
                for w in get_tagset(k - 2):
                    if e[x[k]][v] != 0 and (w, u, v) in q:
                        cur_value = pi[(k - 1, w, u)] + q[(w, u, v)] + e[x[k]][v]
                        if cur_value > max_value:
                            max_value = cur_value
                            arg_max = w
                pi[(k, u, v)] = max_value
                bp[(k, u, v)] = arg_max

    u_last = v_last = ""
    max_value = float("-inf")
    for u in get_tagset(n - 2):
        for v in get_tagset(n - 1):
            if (u, v, "STOP") in q:
                cur_value = pi[(n - 1, u, v)] + q[(u, v, "STOP")]
                if cur_value > max_value:
                    max_value = cur_value
                    u_last = u
                    v_last = v

    tag_sequence = [''] * n
    tag_sequence[-1] = v_last
    if n > 1:
        tag_sequence[-2] = u_last

    for k in range(n - 3, -1, -1):
        tag_sequence[k] = bp[(k + 2, tag_sequence[k + 1], tag_sequence[k + 2])]

    prob = []
    for k in range(n):
        if k < 1:
            prob.append(pi[(0, "*", tag_sequence[k])])
        else:
            prob.append(pi[(k, tag_sequence[k - 1], tag_sequence[k])])
    return tag_sequence, prob

if __name__ == "__main__":
    running_time = time.time()
    tags = get_available_tags()
    q = get_transition_prob()
    e = get_emission_prob()
    tagger()
    running_time = time.time() - running_time
    print "running_time: %.8f" % (running_time)
