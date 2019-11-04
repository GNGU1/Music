# This code is to split data into two sets. Meanwhile, generate necessary corpus.
from sklearn.model_selection import train_test_split

data_list = []  # Contain original data which extracted from txt file.
user_corpus = []  # The corpus for all presented user-pairs, form is [['a', 'b'], ['a', 'c'], ['b', 'c']]
user_song_mapping = {}  # A dict, key = user, value = [song_1, song_2, ...]
average_score = {}  # A dict, key = item, value = average score of this user

a = open("/Users/gordonli/PycharmProjects/music/User-Based/Data/1000.txt", "r")
for ds_line in a:
    data_list = data_list + [ds_line.strip().split('\t')]
a.close()

train, test = train_test_split(data_list, test_size=0.3, random_state=42)

b = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/test.txt", "a+")
for ts_line in range(len(test)):
    for dl_line in range(len(test[ts_line])):
        b.write(test[ts_line][dl_line])
        b.write('\t')
    b.write('\n')
b.close()
test = []


def noisy_data_remove():  # Remove the users which use less than 5 tracks
    global train
    tem_list = []
    for tn_line in range(len(train)):
        tem_list = tem_list + [train[tn_line][0]]
    tem_dict = {}
    for key in tem_list:
        tem_dict[key] = tem_dict.get(key, 0) + 1
    tem_list = []
    for (tf_key, tf_value) in tem_dict.items():
        if tf_value >= 5:  # initial filtering, for removing the users which present less than 5 times
            tem_list = tem_list + [tf_key]
    an_tem_list = []
    for tem_key in range(len(train)):
        if train[tem_key][0] in tem_list:
            an_tem_list = an_tem_list + [train[tem_key]]
    train = an_tem_list
    return train


noisy_data_remove()

c = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/train.txt", "a+")
for tr_line in range(len(train)):
    for sp_line in range(len(train[tr_line])):
        c.write(train[tr_line][sp_line])
        c.write('\t')
    c.write('\n')
c.close()


def user_extraction():
    global user_corpus
    for i in range(len(train)):
        user_corpus = user_corpus + [train[i][0]]
    user_corpus = list(dict.fromkeys(user_corpus))
    return user_corpus


user_extraction()


def user_average_score():
    global average_score
    for h in range(len(user_corpus)):
        user_total_score = 0
        user_len = 0
        for g in range(len(train)):
            if user_corpus[h] in train[g]:
                user_total_score = user_total_score + float(train[g][2])
                user_len = user_len + 1
        user_total_score = user_total_score / user_len
        average_score.update({user_corpus[h]: user_total_score})
    return average_score  # Average score, form: key = user, value = total_score / records number


user_average_score()

d = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/average_score.txt", "a+")
for (as_key, as_value) in average_score.items():
    d.write(as_key)
    d.write(" ")
    d.write(str(as_value) + '\n')
d.close()
average_score = []

e = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_corpus.txt", "a+")
for uc in range(len(user_corpus)):
    e.write(user_corpus[uc] + '\n')
e.close()


def user_song_dict():
    global user_song_mapping
    tem_mapping = {}
    for w in range(len(user_corpus)):
        song_value = []
        for r in range(len(train)):
            if user_corpus[w] in train[r]:
                song_value = song_value + [train[r][1]]
            else:
                song_value = song_value

        tem_mapping.update({user_corpus[w]: song_value})
    user_song_mapping = tem_mapping
    return user_song_mapping  # A dict, each user corresponds to all his/her songs


user_song_dict()

e = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_track_mapping.txt", "a+")
for (m_key, m_value) in user_song_mapping.items():
    e.write(m_key)
    e.write(" ")
    for f in range(len(m_value)):
        e.write(m_value[f])
        e.write(" ")
    e.write('\n')
e.close()
user_song_mapping = []


