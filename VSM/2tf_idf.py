# 1. The objective of this code is to generate vector for each track
# 2. we separate the data as train and test
# 3. The file 'track_list.txt': the track names line by line
# 4. TF.txt: the term frequency of each track. The order same as track_list.txt
# 5. TF_IDF.txt: The term_frequency * inverse_document_frequency. Order same as track_list.txt
# 6. Laplace Smoothing (line 145) for avoiding some term frequency is 0.

import math
from sklearn.model_selection import train_test_split

data = []  # Contains the original data which extracted from data list
track_list = []  # All tracks in the data. same order with data list
words_bag = []  # Final form: [{'a': 1, 'b': 2, ...}, {'b': 4, 'd': 7, ...}]
list_len = []
document_frequency = []  # Inverse document frequency, fixed value
words_vector = []
eu_distance = 0  # The distance between each track pairs


a = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics_final.txt", "r")  # over 200000 records
for line in a:
    data = data + [line.strip().split(' ')]
a.close()

train, test = train_test_split(data, test_size=0.3, random_state=42)
data = train

train_creation = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/train.txt",
                      "a+")
for ppp in range(len(train)):
    for ee in range(len(train[ppp])):
        train_creation.write(train[ppp][ee])
        train_creation.write('\t')
    train_creation.write('\n')

train_creation.close()


test_creation = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/test.txt",
                     "a+")
for qqq in range(len(test)):
    for eee in range(len(test[qqq])):
        test_creation.write(test[qqq][eee])
        test_creation.write('\t')
    test_creation.write('\n')

test_creation.close()


def track_extraction():
    global track_list
    for b in range(len(data)):
        track_list = track_list + [data[b][0]]
    return track_list


track_extraction()


def track_list_generation():
    track = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/track_list.txt",
                 "a+")  # The track list, in order
    for c in range(len(track_list)):
        track.write(track_list[c] + '\n')
    track.close()


track_list_generation()


def words_bag_extraction():
    global words_bag
    noisy_data = []
    for c in range(len(data)):
        noisy_data = noisy_data + [data[c][0]] + [data[c][1]]
    for d in range(len(data)):
        words_bag = words_bag + [[x for x in data[d] if x not in noisy_data]]
    return words_bag


words_bag_extraction()


def dict_generation():
    global words_bag
    tem_bag = []

    for e in range(len(words_bag)):
        tem_single_bag = {}  # The words content for each bag

        for f in range(len(words_bag[e])):
            tem_words = words_bag[e][f].split(':')
            tem_single_bag.update({tem_words[0]: tem_words[1]})
        tem_bag = tem_bag + [tem_single_bag]
    words_bag = tem_bag
    return words_bag


dict_generation()


def value_str_covert():
    global words_bag
    for g in range(len(words_bag)):

        for (v_key, v_value) in words_bag[g].items():
            value = int(v_value)
            words_bag[g][v_key] = value

    return words_bag


value_str_covert()


def sample_list_generation():
    global list_len
    for h in range(1, 5001):
        list_len = list_len + [h]
    for i in range(len(list_len)):
        list_len[i] = str(list_len[i])
    return list_len


sample_list_generation()


def words_array_generation():
    words_array = []  # Representing complete vectors, Form: [[2, 0, ... (5000th)], [3, 1, 2, ... (5000th)]]
    for i in range(len(words_bag)):
        tem_array = []
        for j in range(len(list_len)):
            if list_len[j] in words_bag[i].keys():
                tem_array = tem_array + [words_bag[i][list_len[j]]]
            else:
                tem_array = tem_array + [0]
        words_array = words_array + [tem_array]

    k = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/TF.txt", "a+")
    for m in range(len(words_array)):
        for n in range(len(words_array[m])):
            k.write(str(words_array[m][n]))
            k.write(" ")
        k.write('\n')
    k.close()


words_array_generation()  # TF


def inverse_document_frequency():
    global document_frequency
    words_array = []  # Representing complete vectors, Form: [[2, 0, ... (5000th)], [3, 1, 2, ... (5000th)]]
    for o in range(len(words_bag)):
        tem_array = []
        for p in range(len(list_len)):
            if list_len[p] in words_bag[o].keys():
                tem_array = tem_array + [words_bag[o][list_len[p]]]
            else:
                tem_array = tem_array + [0]
        words_array = words_array + [tem_array]
    for q in range(5000):
        tem_document_frequency = 0
        for r in range(len(words_array)):
            if words_array[r][q] == 0:
                tem_document_frequency = tem_document_frequency
            else:
                tem_document_frequency = tem_document_frequency + 1
        document_frequency = document_frequency + [tem_document_frequency]
    for s in range(len(document_frequency)):
        document_frequency[s] = (document_frequency[s] + 1) / (len(data) + 2)
    for u in range(len(document_frequency)):
        document_frequency[u] = 1 / document_frequency[u]
    for t in range(len(document_frequency)):
        document_frequency[t] = math.log(document_frequency[t])
    return document_frequency


inverse_document_frequency()


def tf_idf():
    term_frequency = []
    u = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/TF.txt", "r")
    for tf in u:
        term_frequency = term_frequency + [tf.strip().split(" ")]
    u.close()

    for v in range(len(term_frequency)):
        for w in range(len(term_frequency[v])):
            term_frequency[v][w] = int(term_frequency[v][w])

    for x in range(len(term_frequency)):
        for y in range(len(term_frequency[x])):
            term_frequency[x][y] = term_frequency[x][y] * document_frequency[y]

    z = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/TF_IDF.txt", "a+")
    for aa in range(len(term_frequency)):
        for ab in range(len(term_frequency[aa])):
            z.write(str(term_frequency[aa][ab]))
            z.write(" ")
        z.write('\n')
    z.close()


tf_idf()






