# 1. this code is to generate necessary lists & dataset
# 2. split the rating data set

from sklearn.model_selection import train_test_split

data_list = []  # The list contains all data
user_corpus = []  # The corpus for containing all users. For further processing

a = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Data/1000.txt", "r")
for data_line in a:
    data_list = data_list + [data_line.strip().split('\t')]
a.close()

train, test = train_test_split(data_list, test_size=0.3, random_state=42)

train_creation = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/train.txt", "a+")
for b in range(len(train)):
    for c in range(len(train[b])):
        train_creation.write(train[b][c])
        train_creation.write('\t')
    train_creation.write('\n')
train_creation.close()

test_creation = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/test.txt", "a+")
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

g = open("C:/Users/s4538443/PycharmProjects/untitled/tfidf/Training Results/user_corpus.txt", "a+")
for h in range(len(user_corpus)):
    g.write(user_corpus[h])
    g.write("\n")
g.close()





