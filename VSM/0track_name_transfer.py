# The purpose of this code is to transfer tracks' name (TR) as songs' name (SO)
# The results are in lyrics_test.txt file

song = []
track = []

a = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics.txt", "r")
for sim_line in a:
    track = sim_line.strip().split(",")

    tem_sim = []

    b = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/transfer.txt", "r")
    for son_line in b:
        song = son_line.strip().split("\t")
        if len(song) == 2:
            if track[0] in song:
                track[0] = song[0]

                c = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics_test.txt", "a+")
                for d in range(len(track)):
                    c.write(track[d])
                    c.write(' ')
                c.close()

                e = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/lyrics_test.txt", "a+")
                e.write(' ' + '\n')
                e.close()

    b.close()

a.close()

