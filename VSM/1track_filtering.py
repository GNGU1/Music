# This code is to remove the tracks which don't appear in our original dataset (1000.txt).
# Reduce workload purpose.
# The tracks which don't appear in the original dataset can not be evaluated.

# 1000.txt refers to the original (user, track, rating) set, not split yet
# track_corpus.txt contains all tracks which present in 1000.txt
# lyrics_test.txt contains the lyrics for each track. The track name has been transferred already.
# lyrics_final.txt is the set which filtered by two steps already.

track_corpus = []
a = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/1000.txt", "r")
for t_line in a:
    track = t_line.strip().split('\t')
    track_corpus = track_corpus + [track[1]]
a.close()

track_corpus = list(dict.fromkeys(track_corpus))

b = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/track_corpus.txt", "a+")
for c in range(len(track_corpus)):
    b.write(track_corpus[c] + '\n')
b.close()


d = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics_test.txt", "r")
for lt_line in d:
    lyrics = lt_line.strip().split(" ")

    e = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/track_corpus.txt", "r")
    for tc_line in e:
        track_line = tc_line.strip()

        if lyrics[0] in track_line:
            f = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics_final.txt", "a+")
            for g in range(len(lyrics)):
                f.write(lyrics[g])
                f.write(' ')
            f.close()
            h = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics_final.txt", "a+")
            h.write(' ' + '\n')
            h.close()

    e.close()

d.close()

