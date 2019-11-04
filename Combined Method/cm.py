ib_corpus = []
ub_corpus = []
ti_corpus = []
user_corpus = []

a = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_prediction.txt", "r")
for ib_line in a:
    ib_corpus = [ib_corpus + [ib_line.strip().split("|")[0] + ib_line.strip().split("|")[1]]]
a.close()

b = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/user_based_prediction.txt", "r")
for ub_line in b:
    ub_corpus = ub_corpus + [[ub_line.strip().split("|")[0] + ub_line.strip().split("|")[1]]]
b.close()

c = open("/Users/gordonli/PycharmProjects/music/Vector Space Model/Training Results/tf_idf_prediction.txt", "r")
for ti_line in c:
    ti_corpus = ti_corpus + [[ti_line.strip().split()[0] + ti_line.strip().split("|")[1]]]
c.close()


def common_user():
    global user_corpus
    tem_dict = {}
    tem_list = []
    user_corpus = ub_corpus + ib_corpus + ti_corpus
    for key in user_corpus:
        tem_dict[key] = tem_dict.get(key, 0) + 1

    for (uc_key, uc_value) in tem_dict.items():
        if uc_value == 3:
            tem_list = tem_list + [uc_key]

    user_corpus = tem_list
    return user_corpus


common_user()


def percentage():
    for d in range(len(user_corpus)):
        ib = float()
        ub = float()
        ti = float()

        ib_num = float()
        ub_num = float()
        ti_num = float()
        total_num = float()

        e = open("test.txt", "r")
        for gt_line in e:
            if user_corpus[d][0] == gt_line.strip().split('\t')[0] and user_corpus[d][1] == gt_line.strip().split('\t')[1]:
                f = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_prediction.txt",
                         "r")
                for an_ib_line in f:
                    if user_corpus[d][0] == an_ib_line.strip().split('\t')[0] and user_corpus[d][1] == an_ib_line.strip().split('\t')[1]:
                        ib = float(an_ib_line.strip().split('\t')[2])
                f.close()

                g = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/user_based_prediction.txt",
                         "r")
                for an_ub_line in g:
                    if user_corpus[d][0] == an_ub_line.strip().split('\t')[0] and user_corpus[d][1] == an_ub_line.strip().split('\t')[1]:
                        ub = float(an_ub_line.strip().split('\t')[2])
                g.close()

                h = open(
                    "/Users/gordonli/PycharmProjects/music/Vector Space Model/Training Results/tf_idf_prediction.txt",
                    'r')
                for an_ti_line in h:
                    if user_corpus[d][0] == an_ti_line.strip().split('\t')[0] and user_corpus[d][1] == an_ti_line.strip().split('\t')[1]:
                        ti = float[an_ti_line.strip().split('\t')]
                h.close()

            ib = (ib - float(gt_line.strip().split('\t')[2])) ** 2
            ub = (ub - float(gt_line.strip().split('\t')[2])) ** 2
            ti = (ti - float(gt_line.strip().split('\t')[2])) ** 2

            if ib > ub:
                if ub > ti:
                    ti_num = ti_num + 1
                else:
                    ub_num = ub_num + 1
            else:
                if ib > ti:
                    ti_num = ti_num + 1
                else:
                    ib_num = ib_num + 1
            total_num = total_num + 1
        e.close()

        """ Laplacian Smoothing"""
        ti = (ti_num + 1) / (total_num + 3)
        ub = (ub_num + 1) / (total_num + 3)
        ib = (ib_num + 1) / (total_num + 3)

        m = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_prediction.txt", "r")
        for ib_final in m:
            if user_corpus[d][0] == ib_final.strip().split('\t')[0] and user_corpus[d][1] == ib_final.strip().split('\t')[1]:
                ti = ti * float(ib_final.strip().split('\t')[2])
        m.close()

        n = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/user_based_prediction.txt", "r")
        for ub_final in n:
            if user_corpus[d][0] == ub_final.strip().split('\t')[0] and user_corpus[d][1] == ub_final.strip().split('\t')[1]:
                ub = ub * float(ub_final.strip().split('\t')[2])
        n.close()

        p = open("/Users/gordonli/PycharmProjects/music/Vector Space Model/Training Results/tf_idf_prediction.txt", "r")
        for ti_final in p:
            if user_corpus[d][0] == ti_final.strip().split('\t')[0] and user_corpus[d][1] == ti_final.strip().split('\t')[1]:
                ti = ti * float(ti_final.strip().split('\t')[2])
        p.close()

        i = open("combined_method.txt", "a+")
        i.write(user_corpus[d][0])
        i.write("|")
        i.write(user_corpus[d][1])
        i.write("|")
        i.write(str(ti + ub + ib) + '\n')
        i.close()


percentage()
