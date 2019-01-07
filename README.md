# NLP-HMM-Viterbi
I built a trigram HMM tagger for named entities.

 - 4_1.py, which produces a new file: ner_train_rare.dat, the data file with_RARE_words. Run count_freqs.py on thener_train_rare.dat to produce the counts filener_rare.counts.
 
 - 4_2.py, which produces 4_2.txt, the tagged ner_dev.dat data with the extra log likelihood column.
 
 - 5_1.py, which produces 5_1.txt, the file containing trigrams and their respective param-eters in the format, “wi2wi1wilogeq(wijwi2; wi1)”. Assume that the file to be read will be called trigrams.txt, and will be located in your root directory. Each line of thistrigrams.txtcontains the trigrams: “wi2wi1wi”.
 
 - 5_2.py, which produces 5_2.txt, the taggedner_dev.datdata in the same format as 4_2.txt but tagged using the Viterbi tagger.
 
 - 5.6.py, which produces6.txt, the taggedner_dev.datdata in the same format as 4_2.txt and 5_2.txt but tagged using the improved Viterbi tagger that better deals with rarewords.
