# This code is to deploy  Pearson correlation similarity
import itertools

user_corpus = []  # The corpus for all presented user-pairs, form is [['a', 'b'], ['a', 'c'], ['b', 'c']]

a = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/user_corpus.txt", "r")
for uc_line in a:
    user_corpus = user_corpus + [uc_line.strip()]
a.close()


def user_based_filtering():
    global u_tem_average_score, v_tem_average_score, r_ui, r_vi, song_candidate

    for user_combination in itertools.combinations(user_corpus, 2):
        user_combination = list(user_combination)
        song_candidate = []

        numerator = 0  # For Pearson correlation Cosine Similarity numerator plus iteration.

        u_denominator = 0  # For Pearson correlation Cosine Similarity denominator item i plus iteration.
        v_denominator = 0  # For Pearson correlation Cosine Similarity denominator item j plus iteration.

        u_tem_average_score = 0  # For user u average rating score. Different from each user.
        v_tem_average_score = 0  # For user v average rating score. Different from each user.

        similarity = 0  # For music combination similarity

        b = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/train.txt", "r")
        for utm_line in b:
            if user_combination[0] in utm_line.strip().split('\t'):
                song_candidate = song_candidate + [utm_line.strip().split('\t')[1]]
            if user_combination[1] in utm_line.strip().split('\t'):
                song_candidate = song_candidate + [utm_line.strip().split('\t')[1]]
        b.close()  # The tracks which rated by these two users

        def candidate_pro():
            global song_candidate
            track_pt = {}  # songs' presence times.
            com_track = []  # Temporary list for containing co-rated songs.
            for can_song in song_candidate:
                track_pt[can_song] = track_pt.get(can_song, 0) + 1

            for (song_key, song_frequency) in track_pt.items():
                if song_frequency == 2:  # For finding common rated songs.
                    com_track = com_track + [song_key]
                else:
                    com_track = com_track
            song_candidate = com_track
            return song_candidate

        candidate_pro()

        if len(song_candidate) >= 5:  # ###Use 5 as threshold for finding similarity###

            d = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/average_score.txt", "r")
            for as_line in d:
                if user_combination[0] in as_line.strip().split(" "):
                    u_tem_average_score = float(as_line.strip().split(" ")[1])
                if user_combination[1] in as_line.strip().split(" "):
                    v_tem_average_score = float(as_line.strip().split(" ")[1])
            d.close()  # Extract these two users' average score

            for c in range(len(song_candidate)):
                #  The iteration for retrieving each song rating
                r_ui = 0  # Denotes the rating of user u on item i
                r_vi = 0  # Denotes the rating of user v on item i

                e = open("/Users/gordonli/PycharmProjects/music/User-Based/Training Results/train.txt", "r")
                for td_line in e:
                    if user_combination[0] in td_line.strip().split('\t') and song_candidate[c] in td_line.strip().split('\t'):
                        r_ui = float(td_line.strip().split('\t')[2])
                    if user_combination[1] in td_line.strip().split('\t') and song_candidate[c] in td_line.strip().split('\t'):
                        r_vi = float(td_line.strip().split('\t')[2])
                e.close()

                numerator = numerator + (r_ui - u_tem_average_score) * (r_vi - v_tem_average_score)
                u_denominator = u_denominator + ((r_ui - u_tem_average_score) ** 2)
                v_denominator = v_denominator + ((r_vi - v_tem_average_score) ** 2)

            if u_denominator != 0 and v_denominator != 0:  # ##### All users gave same score for one track####
                similarity = numerator / ((u_denominator ** 0.5) * (v_denominator ** 0.5))

                if similarity > 0:  # ###Removed the similarity which less than 0.###
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

