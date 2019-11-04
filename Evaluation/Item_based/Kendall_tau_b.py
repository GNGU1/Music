# Line 14: extract data, number is str type
# Line 22: transfer str to float
# Line 26: obtain the candidate users, will be used as dict key
# Line 42: Obtain the necessary data from original_data
# Line 48: Rank all track in current dict_value, based on predicted value
# Line 53: Update the dictionary {user_candidate: dict_value}
original_data = []
user_candidate = []
training_data = {}

original_data_test = []
user_candidate_test = []
test_data = {}

a = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_prediction.txt", "r")

for data_line in a:
    original_data = original_data + [data_line.strip().split("|")]

a.close()

for e in range(len(original_data)):
    original_data[e][2] = float(original_data[e][2])


def extract_user_candidate():
    global user_candidate
    for b in range(len(original_data)):
        user_candidate = user_candidate + [original_data[b][0]]
    user_candidate = list(dict.fromkeys(user_candidate))

    return user_candidate


extract_user_candidate()


def training_data_processing():
    global training_data
    for c in range(len(user_candidate)):
        dict_value = []
        for d in range(len(original_data)):
            if user_candidate[c] == original_data[d][0]:
                dict_value = dict_value + [[original_data[d][1], original_data[d][2]]]
            else:
                dict_value = dict_value

        def takeSecond(elem):
            return elem[1]

        dict_value.sort(reverse=True, key=takeSecond)

        for f in range(len(dict_value)):
            dict_value[f] = dict_value[f][0]

        training_data.update({user_candidate[c]: dict_value})

    return training_data


training_data_processing()


g = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/test.txt", "r")

for test_line in g:
    original_data_test = original_data_test + [test_line.strip().split("\t")]

g.close()


for h in range(len(original_data_test)):
    original_data_test[h][2] = float(original_data_test[h][2])


def test_candidate_extraction():
    global user_candidate_test
    for i in range(len(original_data_test)):
        user_candidate_test = user_candidate_test + [original_data_test[i][0]]
    user_candidate_test = list(dict.fromkeys(user_candidate_test))

    return user_candidate_test


test_candidate_extraction()


def test_data_processing():
    global test_data
    for j in range(len(user_candidate_test)):
        dict_value = []
        for k in range(len(original_data_test)):
            if user_candidate_test[j] == original_data_test[k][0]:
                dict_value = dict_value + [[original_data_test[k][1], original_data_test[k][2]]]
            else:
                dict_value = dict_value

        def takeSecond(elem):
            return elem[1]

        dict_value.sort(reverse=True, key=takeSecond)

        for l in range(len(dict_value)):
            dict_value[l] = dict_value[l][0]

        test_data.update({user_candidate_test[j]: dict_value})


test_data_processing()


def kendall_tau_b():
    global or_track_value, tr_track_value, denominator
    tem_user_count = {}
    tem_users = []
    tem_user_can = []

    kendall_index = 0
    user_number = 0

    for (training_key, training_value) in training_data.items():
        tem_users = tem_users + [training_key]

    for (test_key, test_value) in test_data.items():
        tem_users = tem_users + [test_key]

    for m in tem_users:
        tem_user_count[m] = tem_user_count.get(m, 0) + 1

    for (tem_key, tem_value) in tem_user_count.items():
        if tem_value == 2:
            tem_user_can = tem_user_can + [tem_key]
        else:
            tem_user_can = tem_user_can  # Common users in training_data & test_data

    for n in range(len(tem_user_can)):
        common_track = []
        common_track_count = {}
        track_pair = []  # The common tracks for respective training data & test data

        concordant = 0
        discordant = 0

        or_track_value = []  # Values of common_track in training data
        tr_track_value = []  # Values of common_track in test data

        numerator = 0
        denominator = 0

        for (an_s_key, an_s_value) in test_data.items():
            if tem_user_can[n] == an_s_key:
                common_track = common_track + an_s_value
                track_pair = track_pair + [an_s_value]

        for (an_t_key, an_t_value) in training_data.items():
            if tem_user_can[n] == an_t_key:
                common_track = common_track + an_t_value
                track_pair = track_pair + [an_t_value]

        for o in common_track:
            common_track_count[o] = common_track_count.get(o, 0) + 1

        for (c_key, c_value) in common_track_count.items():
            if c_value != 2:
                common_track.remove(c_key)

        common_track = list(dict.fromkeys(common_track))

        for p in range(len(track_pair)):    # Quantization (From track to float)
            track_pair[p] = [x for x in track_pair[p] if x in common_track]

        for q in range(len(track_pair[0])):
            track_pair[1] = [w.replace(track_pair[0][q], str(q)) for w in track_pair[1]]
            track_pair[0][q] = str(q)

        for r in range(len(track_pair)):
            for s in range(len(track_pair[r])):
                track_pair[r][s] = float(track_pair[r][s])

        compare_list = track_pair[0]

        for t in range(len(track_pair[1])):
            for u in range(len(compare_list)):
                if track_pair[1][t] < compare_list[u]:
                    concordant = concordant + 1
                else:
                    discordant = discordant + 1
            compare_list.remove(track_pair[1][t])

        for u in range(len(common_track)):
            for v in range(len(original_data)):
                if common_track[u] in original_data[v]:
                    or_track_value = or_track_value + [original_data[v][3]]

            for w in range(len(original_data_test)):
                if common_track[u] in original_data_test[w]:
                    tr_track_value = tr_track_value + [original_data_test[w][2]]

        def track_value_statistics():
            global or_track_value, tr_track_value
            or_dict = {}
            tr_dict = {}

            for or_fre in or_track_value:
                or_dict[or_fre] = or_dict.get(or_fre, 0) + 1

            for tr_fre in tr_track_value:
                tr_dict[tr_fre] = tr_dict.get(tr_fre, 0) + 1

            or_track_value = or_dict
            tr_track_value = tr_dict
            return or_track_value, tr_track_value

        track_value_statistics()

        numerator = concordant - discordant

        def denominator_computation():
            global denominator
            f_part = 0
            s_part = 0
            for (or_key, or_value) in or_track_value.items():
                f_part = f_part + or_value * (or_value - 1) / 2
            for (tr_key, tr_value) in tr_track_value.items():
                s_part = s_part + tr_value * (tr_value - 1) / 2

            t_part = len(common_track) * (len(common_track) - 1) / 2
            denominator = ((t_part - f_part) * (t_part - s_part)) ** 0.5

            return denominator

        denominator_computation()

        if denominator != 0:
            kendall_index = kendall_index + numerator / denominator
        else:
            kendall_index = kendall_index
        user_number = user_number + 1

    kendall_index = kendall_index / user_number

    print(kendall_index)


kendall_tau_b()
