# This code is to generate corresponding dataset
import random

user_len = []
r = open("/Users/gordonli/PycharmProjects/music/BPR/Data/1000.txt", "r")
for fl_line in r:
    data_filter = fl_line.strip().split('\t')
    user_len = user_len + [data_filter[0]]
r.close()


def filtering():
    global user_len
    term_fre = {}
    c_user = []
    for key in user_len:
        term_fre[key] = term_fre.get(key, 0) + 1
    for (term_key, term_value) in term_fre.items():
        if term_value >= 20:
            c_user = c_user + [term_key]
    user_len = c_user
    return user_len


filtering()

for t in range(len(user_len)):
    u = open("/Users/gordonli/PycharmProjects/music/BPR/Data/1000.txt", "r")
    for tem_line in u:
        if user_len[t] in tem_line.strip().split('\t'):
            s = open("/Users/gordonli/PycharmProjects/music/BPR/data/data.txt", "a+")
            s.write(tem_line.strip().split('\t')[0])
            s.write('\t')
            s.write(tem_line.strip().split('\t')[1])
            s.write('\t')
            s.write(tem_line.strip().split('\t')[2] + '\n')
            s.close()
    u.close()
user_len = []


user_corpus = []
a = open("/Users/gordonli/PycharmProjects/music/BPR/Data/data.txt", "r")
for d_line in a:
    data = d_line.strip().split("\t")
    user_corpus = user_corpus + [data[0]]
a.close()
user_corpus = list(dict.fromkeys(user_corpus))  # All users

c = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/users.dat", "a+")
for b in range(1, len(user_corpus) + 1):
    c.write(str(b))
    c.write("::")
    c.write("F")
    c.write("::")
    c.write(str(random.randint(1, 60)))
    c.write("::")
    c.write(str(random.randint(0, 20)))
    c.write("::")
    c.write(str(random.randint(10000, 99999)) + '\n')
c.close()

e = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/user_map.dat", "a+")
for d in range(1, len(user_corpus) + 1):
    e.write(user_corpus[d-1])
    e.write(" ")
    e.write(str(d) + '\n')
e.close()
user_corpus = []


user_tracks = []
f = open("/Users/gordonli/PycharmProjects/music/BPR/Data/data.txt", "r")
for t_line in f:
    user_tracks = user_tracks + [t_line.strip().split("\t")[1]]
f.close()

user_tracks = list(dict.fromkeys(user_tracks))

g = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/movies.dat", "a+")
for h in range(len(user_tracks)):
    g.write(str(h+1))
    g.write("::")
    g.write(user_tracks[h])
    g.write("::")
    g.write("hello world" + '\n')
g.close()
user_tracks = []


j = open("/Users/gordonli/PycharmProjects/music/BPR/data/data.txt", "r")
for r_line in j:
    line = r_line.strip().split('\t')

    user = line[0]
    m = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/user_map.dat", "r")
    for um_line in m:
        um = um_line.strip().split(" ")
        if user in um:
            n = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/ratings.dat", "a+")
            n.write(um[1])
            n.write("::")
            n.close()
    m.close()

    track = line[1]
    o = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/movie.dat", "r")
    for tk_line in o:
        tk = tk_line.strip().split("::")
        if track in tk:
            p = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/rating.dat", "a+")
            p.write(tk[0])
            p.write("::")
            p.close()
    o.close()

    q = open("/Users/gordonli/PycharmProjects/music/BPR/data/ml-1m/rating.dat", "a+")
    q.write(line[2])
    q.write("::")
    q.write(str(random.randint(10000, 99999)) + '\n')
    q.close()

j.close()
