
"""  Hybrid Recommender """


import pandas as pd
pd.set_option('display.max_columns', 5)

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('../input/movielens-20m-dataset/movie.csv')
    rating = pd.read_csv('../input/movielens-20m-dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()


# Determine the movies watched by the user to be suggested.
random_user = 108170
random_user_df = user_movie_df[user_movie_df.index == random_user]
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
movies_watched
len(movies_watched)

# We need to go to watch movies that a random user is watching.


# You access the data and Ids of users broadcasting from the same players
movies_watched_df = user_movie_df[movies_watched]
movies_watched_df.head()
# line above is the movie 138493 that says the same thing as this person.
#There is someone who watched at least 1 of these 186 movies.
# not work . There must be users watching your en few packages.
# 1 watching doesn't show the same behavior pattern as this person
movies_watched_df.shape


user_movie_count = movies_watched_df.T.notnull().sum()
# where all users have discovered how many discoveries
# In the output, we reached the information of how many movies the user of each user watched.
# user movie counts have arrived.

user_movie_count = user_movie_count.reset_index()
# We saved the index of user ids. We converted them to variables.
# and has information about how many movies he has watched in total in user usages
user_movie_count
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count.head()


perc = len(movies_watched) * 60 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
# who has more common views than random users

users_same_movies.head()
users_same_movies.count()


# In the most similar way to the user to be suggested
final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                      random_user_df[movies_watched]])

final_df.shape
# (2327,186) There are 2327 users. We also have 186 movies


# so far, we have created a subset like that, and we brought random users and those who watch similar movies by more than 60 percent. There is no similarity in behavior at the moment, there is only watching the same movies, I don't know whether you like it or not.

corr_df = final_df.T.corr().unstack().sort_values()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()


# make a choice when shopping 65 percent or more with random users
top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65) & (corr_df["user_id_2"] != random_user)][
    ["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)
top_users

top_users.rename(columns={"user_id_2": "userId"}, inplace=True)
top_users
# it should show the most similar behavior with the random user now
# now we need to go to the rating table of these users. now only on duty.


rating = pd.read_csv('../input/movielens-20m-dataset/rating.csv')
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
# We have merged.. We have merged the top users list with the userid, movie id and rating in your table.
# random user has the highest annual.65+ and apply for them
#measurements and which movie they rated

top_users_ratings.head()
# users, movies and given points..

# Calculate WeightedAverageAdvicePoints and keep the first 5 movies
# we are also with you.

top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
# at the weight center ceremonies singularized according to the movies

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()


recommendation_df[recommendation_df["weighted_rating"] > 4]
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 4].sort_values("weighted_rating", ascending=False)[0:5]

movie = pd.read_csv('../input/movielens-20m-dataset/movie.csv')
movies_to_be_recommend.merge(movie[["movieId", "title"]]).index


# Item Based Suggestion
# According to the name of the movie that the user gave the most recent highest rating from their movies
# Suggest 5 user-based, 5 item-based
user = 108170
movie = pd.read_csv('../input/movielens-20m-dataset/movie.csv')
rating = pd.read_csv('../input/movielens-20m-dataset/rating.csv')


# Users with the most up-to-date ratings from movies that have given 5 points from
# movie recommendation users:
movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)]. \
    sort_values(by="timestamp", ascending=False)["movieId"][0:1].values[0]


def item_based_recommender(movie_name, user_movie_df):
    movie = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)

movies_from_item_based = item_based_recommender(movie[movie["movieId"] == movie_id]["title"].values[0], user_movie_df)

movies_from_item_based[1:6].index.to_list()








