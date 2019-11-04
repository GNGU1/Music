# this code is to generate necessary lists & dataset

from sklearn.model_selection import train_test_split

data_list = []  # The list contains all data
user_corpus = []  # The corpus for containing all users. For further processing
user_song_mapping = {}  # A dict, key = user, value = [song_1, song_2, ...]
average_score = {}  # A dict, key = user, value = average score of this user


a = open("/Users/gordonli/PycharmProjects/music/Item-Based/Data/1000.txt", "r")
for data_line in a:
    data_list = data_list + [data_line.strip().split('\t')]
a.close()


train, test = train_test_split(data_list, test_size=0.3, random_state=42)


def noisy_data_remove():  # Remove the tracks which present less than 3 times
    global train
    tem_list = []
    for line in range(len(train)):
        tem_list = tem_list + [train[line][1]]
    tem_dict = {}
    for key in tem_list:
        tem_dict[key] = tem_dict.get(key, 0) + 1
    tem_list = []
    for (tf_key, tf_value) in tem_dict.items():
        if tf_value >= 5:  # initial filtering, for removing the terms which present less than 5 times
            tem_list = tem_list + [tf_key]
    an_tem_list = []
    for tem_key in range(len(train)):
        if train[tem_key][1] in tem_list:
            an_tem_list = an_tem_list + [train[tem_key]]
    train = an_tem_list
    return train


noisy_data_remove()


train_creation = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/train.txt", "a+")
for b in range(len(train)):
    for c in range(len(train[b])):
        train_creation.write(train[b][c])
        train_creation.write('\t')
    train_creation.write('\n')
train_creation.close()


test_creation = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/test.txt", "a+")
for d in range(len(test)):
    for e in range(len(test[d])):
        test_creation.write(test[d][e])
        test_creation.write('\t')
    test_creation.write('\n')
test_creation.close()

data_list = train
train = []
test = []

for f in range(len(data_list)):
    user_corpus = user_corpus + [data_list[f][0]]
user_corpus = list(dict.fromkeys(user_corpus))


g = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/user_corpus.txt", "a+")
for h in range(len(user_corpus)):
    g.write(user_corpus[h])
    g.write("\n")
g.close()


def user_song_dict():
    global user_song_mapping
    tem_mapping = {}
    for i in range(len(user_corpus)):
        song_value = []
        for j in range(len(data_list)):
            if user_corpus[i] in data_list[j]:
                song_value = song_value + [data_list[j][1]]

        tem_mapping.update({user_corpus[i]: song_value})
    user_song_mapping = tem_mapping
    return user_song_mapping  # A dict, each user corresponds to all his/her songs


user_song_dict()


k = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/user_track_mapping.txt", "a+")
for (users, tracks) in user_song_mapping.items():
    k.write(users)
    k.write(" ")
    for l in range(len(tracks)):
        k.write(tracks[l])
        k.write(" ")
    k.write('\n')
k.close()
user_song_mapping = []


def user_average_score():
    global average_score
    for m in range(len(user_corpus)):
        user_total_score = 0
        user_len = 0
        for n in range(len(data_list)):
            if user_corpus[m] in data_list[n]:
                user_total_score = user_total_score + float(data_list[n][2])
                user_len = user_len + 1
        average_score.update({user_corpus[m]: user_total_score / user_len})
    return average_score  # Average score, form: key = user, value = total_score / records number


user_average_score()


o = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/average_score.txt", "a+")
for (as_track, as_score) in average_score.items():
    o.write(as_track)
    o.write(" ")
    o.write(str(as_score) + '\n')
o.close()
average_score = []
user_corpus = []
