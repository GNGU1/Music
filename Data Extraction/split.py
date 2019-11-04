from sklearn.model_selection import train_test_split
import itertools

data_list = []

a = open("1000.txt", "r")
for line in a:
    data_list = data_list + [line.strip().split('\t')]
a.close()

train, test = train_test_split(data_list, test_size=0.3, random_state=42)

data_list = train

www = open("test.txt", "a+")

for qqq in range(len(test)):
    for eee in range(len(test[qqq])):
        www.write(test[qqq][eee])
        www.write('\t')
    www.write('\n')

www.close()

user_corpus = []  # The corpus for all presented user-pairs, form is [['a', 'b'], ['a', 'c'], ['b', 'c']]
music_corpus = []  # The corpus for containing all songs. For further processing
user_song_mapping = {}  # A dict, key = user, value = [song_1, song_2, ...]
average_score = {}  # A dict, key = item, value = average score of this user
noisy_data = []  # A list contains user pair which don't present in all users.

user_similarity = []  # For containing the first function's results.
similarity_candidate = []  # Includes all similar candidates.


def user_extraction():
    global user_corpus
    for i in range(len(data_list)):
        user_corpus = user_corpus + [data_list[i][0]]
    return user_corpus


user_extraction()


def remove_corpus_duplicates():
    global user_corpus
    user_corpus = list(dict.fromkeys(user_corpus))
    return user_corpus  # A corpus within all users present in the dataset


remove_corpus_duplicates()


def user_average_score():
    global average_score
    for h in range(len(user_corpus)):
        user_total_score = 0
        user_len = 0
        for g in range(len(data_list)):
            if user_corpus[h] in data_list[g]:
                user_total_score = user_total_score + int(data_list[g][2])
                user_len = user_len + 1
        average_score.update({user_corpus[h]: (user_total_score + 1) / user_len})  # Laplace Smoothing
    return average_score  # Average score, form: key = user, value = total_score / records number


user_average_score()


def user_song_dict():
    global user_song_mapping
    b = {}
    for w in range(len(user_corpus)):
        song_value = []
        for r in range(len(data_list)):
            if user_corpus[w] in data_list[r]:
                song_value = song_value + [data_list[r][1]]
            else:
                song_value = song_value

        b.update({user_corpus[w]: song_value})
    user_song_mapping = b
    return user_song_mapping  # A dict, each user corresponds to all his/her songs


user_song_dict()


def user_based_filtering():
    global noisy_data, u_tem_average_score, v_tem_average_score, r_ui, r_vi, numerator, u_denominator, v_denominator, \
        similarity

    for user_combination in itertools.combinations(user_corpus, 2):
        user_combination = list(user_combination)
        song_candidate = []

        numerator = 0  # For Pearson correlation Cosine Similarity numerator plus iteration.

        u_denominator = 0  # For Pearson correlation Cosine Similarity denominator item i plus iteration.
        v_denominator = 0  # For Pearson correlation Cosine Similarity denominator item j plus iteration.

        similarity = 0  # For music combination similarity

        for (user, song) in user_song_mapping.items():
            if user_combination[0] == user:
                song_candidate = song_candidate + song
            else:
                song_candidate = song_candidate

            if user_combination[1] == user:
                song_candidate = song_candidate + song
            else:
                song_candidate = song_candidate  # Get all songs in these two users.

        b = {}  # For containing songs' presence times.
        c = []  # Temporary list for containing common songs.
        for can_song in song_candidate:
            b[can_song] = b.get(can_song, 0) + 1

        for (song_key, song_frequency) in b.items():
            if song_frequency == 2:
                c = c + [song_key]
            else:
                c = c
        song_candidate = c

        if song_candidate == []:
            noisy_data = noisy_data + [user_combination]
        else:
            for b in range(len(song_candidate)):
                u_tem_average_score = 0  # For user u average rating score. Different from each user.
                v_tem_average_score = 0  # For user v average rating score. Different from each user.

                r_ui = 0  # r_ui denotes the rating of user u on item i
                r_vi = 0  # r_ui denotes the rating of user v on item i

                def temporary_average_score():
                    global u_tem_average_score, v_tem_average_score
                    u_tem_average_score = average_score[user_combination[0]]
                    v_tem_average_score = average_score[user_combination[1]]
                    return u_tem_average_score, v_tem_average_score

                temporary_average_score()

                def rating_score_search():
                    global r_ui, r_vi
                    for d in range(len(data_list)):
                        if user_combination[0] in data_list[d] and song_candidate[b] in data_list[d]:
                            r_ui = int(data_list[d][2])

                        if user_combination[1] in data_list[d] and song_candidate[b] in data_list[d]:
                            r_vi = int(data_list[d][2])
                    return r_ui, r_vi

                rating_score_search()

                def numerator_computation():
                    global numerator
                    numerator = numerator + (r_ui - u_tem_average_score) * (r_vi - v_tem_average_score)
                    return numerator

                numerator_computation()

                def denominator_computation():
                    global u_denominator, v_denominator
                    u_denominator = u_denominator + ((r_ui - u_tem_average_score) ** 2)
                    v_denominator = v_denominator + ((r_vi - v_tem_average_score) ** 2)
                    return u_denominator, v_denominator

                denominator_computation()

            def similarity_computation():
                global similarity, noisy_data
                if u_denominator == 0 or v_denominator == 0:
                    noisy_data = noisy_data + [user_combination]
                else:
                    similarity = numerator / ((u_denominator ** 0.5) * (v_denominator ** 0.5))
                return similarity

            similarity_computation()

            def file_output():
                z = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_results.txt", "a+")
                z.write(user_combination[0])
                z.write("|")
                z.write(user_combination[1])
                z.write("|")
                z.write(str(similarity) + '\n')
                z.close()

            file_output()


user_based_filtering()


g = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_results.txt", "r")

for lines in g:
    user_similarity = user_similarity + [lines.strip().split('|')]

g.close()


def similarity_corpus_creation():
    global similarity_candidate
    for h in range(len(user_similarity)):
        similarity_candidate = similarity_candidate + [user_similarity[h][0]] + [user_similarity[h][1]]
    similarity_candidate = list(dict.fromkeys(similarity_candidate))
    return similarity_candidate


similarity_corpus_creation()


def recommendation():
    global tem_neighbour
    for i in range(len(similarity_candidate)):

        tem_neighbour = []  # For containing neighbours for each user.

        tem_neighbour_corpus = []  # For containing the songs for all neighbours

        def neighbour_corpus_generation():
            global tem_neighbour
            for j in range(len(user_similarity)):
                if similarity_candidate[i] in user_similarity[j]:
                    tem_neighbour = tem_neighbour + [user_similarity[j][0]] + [user_similarity[j][1]]
                else:
                    tem_neighbour = tem_neighbour
            return tem_neighbour

        neighbour_corpus_generation()

        def neighbour_corpus_processing():
            global tem_neighbour
            tem_neighbour = [x for x in tem_neighbour if x != similarity_candidate[i]]
            tem_neighbour = list(dict.fromkeys(tem_neighbour))
            return tem_neighbour

        neighbour_corpus_processing()

        for o in range(len(tem_neighbour)):
            for (nei_key, nei_value) in user_song_mapping.items():
                if tem_neighbour[o] == nei_key:
                    tem_neighbour_corpus = tem_neighbour_corpus + nei_value
                else:
                    tem_neighbour_corpus = tem_neighbour_corpus

        tem_neighbour_corpus = [x for x in tem_neighbour_corpus if x not in user_song_mapping[similarity_candidate[i]]]

        tem_neighbour_corpus = list(dict.fromkeys(tem_neighbour_corpus))

        for p in range(len(tem_neighbour_corpus)):
            prediction = 0
            reco_numerator = 0
            reco_denominator = 0

            for k in range(len(tem_neighbour)):
                if tem_neighbour_corpus[p] in user_song_mapping[tem_neighbour[k]]:

                    tem_similarity = 0  # the similarity between similarity_candidate[i] and tem_neighbour[k]

                    tem_ave_score = 0

                    tem_neighbour_rating = 0  # Rating from specific neighbour for specific song

                    for l in range(len(user_similarity)):
                        if tem_neighbour[k] in user_similarity[l] and similarity_candidate[i] in user_similarity[l]:
                            tem_similarity = float(user_similarity[l][2])
                        else:
                            tem_similarity = tem_similarity

                    for (tem_key, tem_value) in average_score.items():
                        if tem_key == tem_neighbour[k]:
                            tem_ave_score = float(tem_value)
                        else:
                            tem_ave_score = tem_ave_score

                    for m in range(len(data_list)):
                        if tem_neighbour[k] in data_list[m] and tem_neighbour_corpus[p] in data_list[m]:
                            tem_neighbour_rating = data_list[m][2]
                        else:
                            tem_neighbour_rating = float(tem_neighbour_rating)

                    reco_numerator = reco_numerator + tem_similarity * (tem_neighbour_rating - tem_ave_score)

                    reco_denominator = reco_denominator + tem_similarity
            if reco_denominator != 0:
                prediction = reco_numerator / reco_denominator

            def file_output():
                n = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_prediction.txt", "a+")
                n.write(similarity_candidate[i])
                n.write("|")
                n.write(tem_neighbour[k])
                n.write("|")
                n.write(tem_neighbour_corpus[p])
                n.write("|")
                n.write(str(prediction) + '\n')
                n.close()

            file_output()


recommendation()
