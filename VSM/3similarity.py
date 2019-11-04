# we use L2-Norm to calculate track similarity

import itertools
# words_bag; Complete bag, Form: [track_name, {W1: F1, W2: F2, ...}]

words_bag = []
_ = []
a = open('C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/track_list.txt', "r")

for track_line in a:
    words_bag = words_bag + [track_line.strip().split(" ")]

a.close()

b = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/TF_IDF.txt", "r")

for tf_line in b:
    _ = _ + [tf_line.strip().split(" ")]

b.close()

for c in range(len(words_bag)):
    words_bag[c] = words_bag[c] + [_[c]]

for d in range(len(words_bag)):
    for e in range(len(words_bag[d][1])):
        words_bag[d][1][e] = float(words_bag[d][1][e])


def similarity():
    track_list = []  # Contain the all track candidates

    for f in range(len(words_bag)):
        track_list = track_list + [words_bag[f][0]]

    for track_combination in itertools.combinations(track_list, 2):  # Contain each track combination
        track_combination = list(track_combination)

        words_combination = []  # Corresponding tracks' words vector. Form: [[w1, w2, ...], [w1, w2, ...]]
        eu_distance = 0    # the distance between these two tracks

        for g in range(len(track_combination)):
            for h in range(len(words_bag)):
                if track_combination[g] in words_bag[h]:
                    words_combination = words_combination + [words_bag[h][1]]
                else:
                    words_combination = words_combination

        for i in range(5000):
            eu_distance = eu_distance + (words_combination[0][i] - words_combination[1][i]) ** 2
        eu_distance = eu_distance ** 0.5

        j = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/similarity.txt",
                 "a+")
        j.write(track_combination[0])
        j.write("|")
        j.write(track_combination[1])
        j.write("|")
        j.write(str(eu_distance) + '\n')
        j.close()


similarity()






