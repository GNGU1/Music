# The code is to deploy Root Mean Square Error

numerator = 0  # The iterative plus of the minus between actual_rate and target_rate
denominator = 0  # The number of co-occurrence (user, tracks) pairs
result = 0

a = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/item_based_prediction.txt", "r")
for tr_line in a:
    target_user = [tr_line.strip().split("|")[0]]
    target_track = [tr_line.strip().split("|")[1]]
    target_rate = float(tr_line.strip().split("|")[2])
    actual_rate = 0

    b = open("/Users/gordonli/PycharmProjects/music/Item-Based/Training Results/test.txt", "r")
    for ts_line in b:
        if target_user[0] in ts_line.strip().split("\t") and target_track[0] in ts_line.strip().split("\t"):
            actual_rate = float(ts_line.strip().split("\t")[2])
            numerator = numerator + (target_rate - actual_rate) ** 2
            denominator = denominator + 1
    b.close()

a.close()

if denominator != 0:
    result = (numerator / denominator) ** 0.5

print(result)
