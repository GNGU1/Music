# Music
The code is for Music Recommendation system

Item based

we use Adjusted cosine similarity

we use Laplace Smoothing for the average score r-. Because some users rating all songs as same value. it will cause

some the average score same as rating value.

In other words, it indicates (1) that this song pair only presents in a one user,
                             (2) and this user rating all songs as same value.

It suggests that the data from this user fundamentally is noisy data

设计recommendation 的思路：
1. 先找到该用户所评估过的所有的歌曲
2. 每首歌所对应的 similarity （在item_based_results.txt 中）都放在一个list中。
这一步保证了我们找到的所有结果都会有neighbour。 如果一组similarity中的两首歌都没有rate，那么这组内容和该用户无关
3. 这时我们可以基于这个list将其分为听过的和没听过的
4. 这时再分别循环这两个list，用similarity去预测那些没听过的歌的评分

整体的思路：
1. we use sklearn.model_selection to split data. The training set and test set are 0.7 and 0.3 respectively. Random state is 42
2. we remove the tracks which present less than 5 times as de-noising measure.
3. 2. we use 2692 records which including (user \t track \t rating)
4. The further list/corpus generation, such as average score, user corpus and user_track_mapping, are based on filtered train dataset
5. we use 5 as threshold. each particular track should present over 5 times. we use this measure for avoiding particular inaccurate rating effect results
6. for prediction, we remove the value which less than 0. we regard them as non-desired recommendation


Item-based Prediction

1.	The original dataset contains 200,361 records, including 12608 users.
2.	We use sklearn package to split data as train and test parts. The test size is 0.3 and train size is 0.7. The random state is 42
3.	For item-based similarity, we remove the RECORDS which its track presents less 10 times. This method is to reduce the computer workload. Since the further similarity iteration requires at least 10 times.
4.	After the split process and remove the tracks which present less 10 times duration, it contains 12608 users, train dataset contains 47,965 records, and test contains 60109 records
5.	The reason why the train set is less than test records is because the we deploy the reduced-workload-method only on the train dataset. In this case, the user corpus and user track mapping are extracted based on the train dataset. However, we didn’t use this manner on test set. We try to remain most possible records in test sets so which can be used for further prediction.

6.	Similarity process. The tracks which present over 10 times is combined as a dataset. We iterate each combination. 
7.	The method is to ensure each track-pair iterates at least 10 times. We use this measure as a de-noising measure since we considered that some tracks might be rated doesn’t reflects users’ actual preference. 
8.	We used adjusted cosine similarity
9.	For avoiding a situation that some particular users rate all tracks as same value. We use Laplace Smoothing for the average score r-. Because some users rating all songs as same value. it will cause
10.	Similar with the BPR, we can actually draw a curve which use the candidate presence time as x-ay, while use the prediction results as the y-ay.
11. The method is same as the "long tail" book stated


10 times iteration (at least):

Data size:             200361 records

Tracks' Similarity:    456 redords 

Prediction Number:     133365 records

Users' Number:         12608 Users

Track's Number:        62950 Tracks

Test set size:         60109 records

Train set size:        47965 records


the RMSE result is: 28.8997603281229










TF-IDF (VECTOR SPACE MODEL)
The lyrics data is developed by different groups. In this case, data sparisity is very obvious.
The most labour-intensive processEs:
1. traiing tracks' similarity (if track number is 10000, the similarity size is C2, 10000) 
2. Use similareity results to recommend target tracks to users

The method is:
1. Transfer the track id (lyrics,txt) to song id (lyrics,txt). This process used the transfer,txt and lyrics.txt. We generated a lyrics_test.txt data. There are total 8909 tracks. In this case, we only need to run these 8909 tracks. If we calculate the similarity first, each track are required to transfer many times.
2. Remove the tracks which doesn't appear in rating dataset. Owning to Adjusted cosine similarity features, the reconmmendation is only availiable in rated tracks. The generated set is in lyrics_final.txt
3. tf-idf method. The text data has been trained. The bag of words contains 5000 words.
4. Generate vector for each track. Owning the size of bag of words, each vector contains 5000 dimensions.
5. the term frequency refers to the presence times in a particular track of a words.
6. tf-idf : The term_frequency * inverse_document_frequency
7. After created vector for each track, we use L2-Norm to calculate the similareity betweent each tracks.
8. The above entire procees replace the Adjusted consine similarity.
9. The further process is same as item-based recommendation


1. the first code is to generate necessary lsit/corpus, and generate vector for each track

2. we split the data into 2 dataset. However, this process seemingly not necessary

3. the train dataset and test set are 0.7 and 0.3 respectively. Random state is 42.

3. each vector contains 5000 dimensions. For each dimension, we use tf-idf for representing its weight

4. we use Euclidean norm (L2-Norm) for calculating the similarity.

5. (The detailed VSM can be checked in data mining slides)

6. In other words, we use tf-idf to replace adjusted cosine similarity, Pearson similarity.

7. After we got item similarity, we use the previous collaborative filtering algorithms to make a prediction

8. we split the rating dataset into 0.7 and 0.3, random state as 42.

9. In this duration, we didn't use the previous de-noising measure, since the previous de-noising measure to improve
the similarity accuracy. we don't need that since we no longer use them for similarity

10. the forth code is to transfer song to track. they are represented by different id but refer to same item

11. the recommendation is same as the item-based recommendation.

12. we also removed the prediction value which less than 0, since we think that the recommendation should not Negative correlation












User based

We use Pearson correlation similarity.

The rough method process is:
(1) Get a series of user pairs
(2) Find common songs for each user pair
(3) Calculate the average score for each song.

The formula is:

https://en.wikipedia.org/wiki/Collaborative_filtering

ru,i denotes the rating of user u in item i
rv,i denotes the rating of user v in item i

ri` denotes the average score of one song in different users

详细过程：
1. we use sklearn.model_selection to split data. The training set and test set are 0.7 and 0.3 respectively. Random state is 42

2. we use 2692 records which including (user \t track \t rating)

3. we remove the user-track pairs which present less than 5 times. The initial de-noising measure.

4. The de-noising measure is adopted on 'train' dataset. the further average score, user_corpus, user_track_mapping are based on the train set.

5. we use Pearson correlation Cosine to calculate similarity.

6. we use 5 as threshold. This threshold is to ensure that each user pair has 5 common rated songs. de-noising measure
(we find user similarity already. However, these users don't have enough common tracks for further prediction. This must
be a big thing if we wish to satisfy: these users' similariy has calculated; under the similarity, at least 3 users have
common tracks. So I guess we can find the best parameters for getting results)


###### 此时，我们的办法是用皮尔森相关系数， adjusted cosine similarity 和推荐过程取最优参数，我们把不同结果的参数的结果带入线性回归求最优解


7. we remove the set which the denominator is 0. This case indicates that these two users has same preference. We regard this situation as 1. same user, 2. impossible

8. we only keep the user similarity which over 0. This measure is because the Pearson characteristics. The Pearson similarity range is [-1, 1], which -1 suggests these two users are absolutely different

9. For finding the prediction, we at least use over 3 users who have common tracks.







LDA

First step is to create several different topics, each one within words distribution
导入sklearn 包， 分析分析算法的性质。




Lyrics Matrix Factorization

the euclidean_distance.txt contains the distance between each track pairs

the track_array.txt contains each track combination

euclidean_distance.txt corresponds to track_array.txt

the words_array.txt contains the bag of words, without duplicates

potential risk is the order for each track and its corresponding distance.

Biggest problem is the very long traing duration. Owning to the big dataset.

Currently We just got the music similarity, for further recommendation, we need to use other algorithms



User-Based Evaluation

We use Kendall rank correlation coefficient Tau -- b to evaluate the results

we used 10003 records
results is:
(0.010925072953754493-6.165333437643399e-05j)



1. 将初步得到的similarity results 中的所有tracks 组成corpus
2. 基于 (data_list) 找到target user没有评估的歌曲
3. 找到common 评估的内容，去循环


 
