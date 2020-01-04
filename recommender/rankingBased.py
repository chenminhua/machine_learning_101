from ast import literal_eval
import pandas as pd
import numpy as np
import pickle

movie_data = pd.read_csv('../data/the-movies-dataset/movies_metadata.csv')
# 共45466部电影，每部电影有24种属性

# genres 流派数据清洗
movie_data['genres'] = movie_data['genres'].fillna('[]').apply(literal_eval).apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
movie_data['year'] = pd.to_datetime(movie_data['release_date'], errors='coerce').apply(
    lambda x: str(x).split('-')[0] if x != np.nan else np.nan)


# Weighted Rating (WR) = $(\frac{v}{v + m} . R) + (\frac{m}{v + m} . C)$
# where,
# * *v* is the number of votes for the movie
# * *m* is the minimum votes required to be listed in the chart
# * *R* is the average rating of the movie
# * *C* is the mean vote across the whole report
vote_counts = movie_data[movie_data['vote_count']
                         .notnull()]['vote_count'].astype('int')
vote_averages = movie_data[movie_data['vote_average']
                           .notnull()]['vote_average'].astype('int')
C = vote_averages.mean()

# quantile表示分位数，用于筛除评分人数太少的电影， 此处为434
m = vote_counts.quantile(0.95)

qualified = movie_data[(movie_data['vote_count'] >= m)
                       & (movie_data['vote_count'].notnull())
                       & (movie_data['vote_average'].notnull())][[
                           'title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')


def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)


qualified['wr'] = qualified.apply(weighted_rating, axis=1)

qualified = qualified.sort_values('wr', ascending=False).head(250)

s = movie_data.apply(lambda x: pd.Series(x['genres']),
                     axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genre'
gen_md = movie_data.drop('genres', axis=1).join(s)
gen_md.head()


def build_chart(genre, percentile=0.85):
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()
                       ]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)

    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (
        df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')

    qualified['wr'] = qualified.apply(lambda x: (
        x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)

    return qualified


for genre in s.unique():
    if genre == "Carousel Productions":
        exit()
    else:
        with open("./data/" + genre, 'wb+') as f:
            pickle.dump(build_chart(genre), f)
            print(genre)

# print(build_chart('Romance').head(15))
