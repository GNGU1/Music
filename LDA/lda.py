from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

data = []
track_list = []
words_bag = []
list_len = []
words_array = []

a = open("lyrics_test.txt", "r")

for line in a:
    data = data + [line.strip().split(",")]

a.close()


def track_extraction():
    global track_list
    for b in range(len(data)):
        track_list = track_list + [data[b][0]]
    return track_list


track_extraction()


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


def array_generation():
    global words_array
    for i in range(len(words_bag)):
        tem_array = []
        for j in range(len(list_len)):
            if list_len[j] in words_bag[i].keys():
                tem_array = tem_array + [words_bag[i][list_len[j]]]
            else:
                tem_array = tem_array + [0]
        words_array = words_array + [tem_array]
    return words_array


array_generation()


words_array = np.floor(words_array)


lda = LatentDirichletAllocation(n_components=10, random_state=0)  # We have 10 topics

print(lda.fit(words_array))

print(lda.components_)

print(lda.bound_)

print(lda.evaluate_every)
