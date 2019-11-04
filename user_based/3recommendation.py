# This code is to make prediction

user_similarity = []  # For containing the first function's results.
similarity_candidate = []  # Includes all similar users.

# All users in the user similarity data set.
a = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_results.txt", "r")
for lines in a:
    similarity_candidate = similarity_candidate + [lines.strip().split('|')[0]] + [lines.strip().split('|')[1]]
a.close()
similarity_candidate = list(dict.fromkeys(similarity_candidate))


def recommendation():
    global neighbour, neighbour_tracks
    for b in range(len(similarity_candidate)):
        neighbour = []  # All neighbours of target user
        neighbour_tracks = []  # All neighbours' rated tracks
        target_as = 0  # The target user's average score

        sc = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/average_score.txt", "r")
        for as_line in sc:
            if similarity_candidate[b] in as_line.strip().split(" "):
                target_as = float(as_line.strip().split(" ")[1])
        sc.close()

        def neighbour_corpus():
            global neighbour
            c = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_results.txt", "r")
            for ubr_line in c:
                if similarity_candidate[b] in ubr_line.strip().split("|"):
                    neighbour = neighbour + [ubr_line.strip().split("|")[0]] + [ubr_line.strip().split("|")[1]]
            c.close()
            neighbour = [x for x in neighbour if x != similarity_candidate[b]]
            # Method: Find all target user and its neighbours. Remove target user
            neighbour = list(dict.fromkeys(neighbour))
            return neighbour

        neighbour_corpus()

        # All rated tracks of its neighbours.
        d = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/train.txt", "r")
        for e in range(len(neighbour)):
            for tr_line in d:
                if neighbour[e] == tr_line.strip().split('\t')[0]:
                    neighbour_tracks = neighbour_tracks + [tr_line.strip().split('\t')[1]]
        d.close()

        # The target of this following function is to:
        # 1. find this user's all neighbour
        # 2. find all its neighbours' tracks, stored in tem_neighbour_corpus
        # 3. remove the tracks which are rated by target user in this list. the unrated tacks are for prediction
        # 4. these tracks should present over 5 times in these neighbours.
        def neg_tracks_prs():
            global neighbour_tracks
            target_tracks = []  # Target user's tracks
            tem_dict = {}  # tf of unrated tracks in neighbours

            f = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_track_mapping.txt", "r")
            for utm_line in f:
                if similarity_candidate[b] == utm_line.strip().split(" ")[0]:
                    for g in range(1, len(utm_line.strip().split(" "))):
                        target_tracks = target_tracks + [utm_line.strip().split(" ")[g]]
            f.close()  # The target user's rated tracks

            neighbour_tracks = [x for x in neighbour_tracks if x not in target_tracks]

            for key in neighbour_tracks:
                tem_dict[key] = tem_dict.get(key, 0) + 1

            tem_nt = []
            for (nc_key, nc_value) in tem_dict.items():
                if nc_value >= 1:
                    tem_nt = tem_nt + [nc_key]
            neighbour_tracks = tem_nt
            return neighbour_tracks

        neg_tracks_prs()

        for m in range(len(neighbour_tracks)):
            prediction = 0
            reco_numerator = 0
            reco_denominator = 0

            def neigh_precessing():
                global neighbour
                tem_neg = []
                for t in range(len(neighbour)):
                    n = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_track_mapping.txt",
                             "r")
                    for utm_line in n:
                        if neighbour[t] in utm_line.strip().split(" ") and neighbour_tracks[m] in utm_line.strip().split(" "):
                            tem_neg = tem_neg + [neighbour[t]]
                    n.close()
                neighbour = tem_neg
                return neighbour

            neigh_precessing()

            if len(neighbour) >= 1:  # This parameter is same as line 73 par. Indicates hwo many users to use
                for h in range(len(neighbour)):
                    # Open the average score to find particular neighbour average score
                    # Open the train to find the rating under (neighbour_tracks[g], neighbour[h])
                    # Open the item_based_results.txt to find the similarity

                    tem_ave_score = 0
                    tem_similarity = 0  # the similarity between neighbour_tracks[g] and neighbour[h]
                    tem_rating = 0  # Rating from specific neighbour for specific song

                    i = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/average_score.txt", "r")
                    for ut_line in i:
                        if neighbour[h] in ut_line.strip().split(" "):
                            tem_ave_score = float(ut_line.strip().split(" ")[1])
                    i.close()

                    j = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/train.txt", "r")
                    for t_line in j:
                        if neighbour[h] in t_line.strip().split("\t") and neighbour_tracks[m] in t_line.strip().split("\t"):
                            tem_rating = float(t_line.strip().split("\t")[2])
                    j.close()

                    k = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_results.txt", "r")
                    for ub_line in k:
                        if neighbour[h] in ub_line.strip().split("|") and similarity_candidate[b] in ub_line.strip().split("|"):
                            tem_similarity = float(ub_line.strip().split("|")[2])
                    k.close()

                    reco_numerator = reco_numerator + tem_similarity * (tem_rating - tem_ave_score)
                    reco_denominator = reco_denominator + tem_similarity

                if reco_denominator != 0:
                    prediction = reco_numerator / reco_denominator + target_as

                    if prediction > 0:
                        def file_output():
                            n = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_based_prediction.txt", "a+")
                            n.write(similarity_candidate[b])
                            n.write("|")
                            n.write(neighbour_tracks[m])
                            n.write("|")
                            n.write(str(prediction) + '\n')
                            n.close()

                        file_output()


recommendation()



