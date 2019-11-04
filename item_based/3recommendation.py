# This code is to make recommendation

music_corpus = []  # The corpus for all presented song-pairs, form is [['a', 'b'], ['a', 'c']]
users_corpus = []  # The corpus for containing all users. For further processing
user_song_mapping = {}  # A dict, key = user, value = [song_1, song_2, ...]
average_score = {}  # A dict, key = user, value = average score of this user
noisy_data = []  # A list contains songs pair which don't present in all users.
item_similarity = []  # The data extracted from first function


# a = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_results.txt", "r")
# for is_line in a:
#     item_similarity = item_similarity + [is_line.strip().split('|')]
# a.close()
#
# for an_flt in range(len(item_similarity)):
#     item_similarity[an_flt][2] = float(item_similarity[an_flt][2])


def recommendation():
    global rated_tracks, unrated_tracks
    b = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/user_corpus.txt", "r")
    for us_line in b:
        sp_user_corpus = us_line.strip().split(" ")
        rated_tracks = []  # The tracks of target use rated
        unrated_tracks = []  # The tracks of target use not rate yet

        def track_split():
            global rated_tracks, unrated_tracks
            tem_tracks = []
            c = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/train.txt", "r")
            for dl_line in c:
                train_list = dl_line.strip().split("\t")
                if sp_user_corpus[0] in train_list:
                    rated_tracks = rated_tracks + [train_list[1]]
            c.close()  # All rated tracks by the target user.

            d = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_results.txt", "r")
            for rs_line in d:
                tem_candidate = rs_line.strip().split("|")
                if tem_candidate[0] in rated_tracks:
                    tem_tracks = tem_tracks + [tem_candidate[0]] + [tem_candidate[1]] # Find the
                if tem_candidate[1] in rated_tracks:
                    tem_tracks = tem_tracks + [tem_candidate[0]] + [tem_candidate[1]]
            d.close()  # The tracks not only is rated, but also within similar tracks
            tem_tracks = list(dict.fromkeys(tem_tracks))
            # Very important. all unrated tracks must have at least one neighbor in the corpus.
            rated_tracks = [x for x in rated_tracks if x in tem_tracks]
            unrated_tracks = [x for x in tem_tracks if x not in rated_tracks]

            return rated_tracks, unrated_tracks

        track_split()

        for j in range(len(unrated_tracks)):
            numerator = 0
            denominator = 0

            for k in range(len(rated_tracks)):
                sim_ij = 0  # The similarity of track i & j
                r_uj = 0  # The rating score of tem_track[k] by user_corpus[h]

                m = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_results.txt", "r")
                for is_line in m:
                    if unrated_tracks[j] in is_line.strip().split("|") and rated_tracks[k] in is_line.strip().split("|"):
                        sim_ij = float(is_line.strip().split("|")[2])
                m.close()

                n = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/train.txt", "r")
                for adl_line in n:
                    data_list = adl_line.strip().split("\t")
                    if rated_tracks[k] in data_list and sp_user_corpus[0] in data_list:
                        r_uj = float(data_list[2])
                n.close()

                numerator = numerator + sim_ij * r_uj
                denominator = denominator + sim_ij

            if denominator != 0:
                prediction = numerator / denominator

                if prediction > 0:
                    def prediction_output():
                        pr = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_prediction.txt", "a+")
                        pr.write(sp_user_corpus[0])
                        pr.write("|")
                        pr.write(unrated_tracks[j])
                        pr.write("|")
                        pr.write(str(prediction) + '\n')
                        pr.close()

                    prediction_output()

    b.close()


recommendation()



