import pandas as pd
import pymongo
import yaml
from pathlib import Path
import os
from rapidfuzz import process

BASE_DIR = Path(__file__).resolve().parent.parent


class MovieNotFoundError(Exception):
    """Raised when the movie is not in database"""

    def __init__(self, movie, message="Movie not in database"):
        self.movie = movie
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.movie} -> {self.message}'


class Recommender:
    """A class used in backend for movie recommendations"""

    def __init__(self, df, conn=None):
        self.conn = conn
        self.data = df

    def recommend(self, movie_title: str, number_of_movies: int = 5,
                  algorithm='from_db'):
        """Recommends any number of movies based on one movie and chosen algorithm"""

        # TODO: Add here other algorithms for recommendations
        #  in form of other methods of the class

        movie_title = self.process_movie_title(movie_title)

        try:
            if algorithm == 'from_db':
                results = self.recommend_tmdb_from_db(movie_title, number_of_movies)
                results = self.find_posters_for_recommendations(results)
            else:
                results = None

            return results, movie_title
        except MovieNotFoundError:  # TODO: think of a way to cope with this
            return None

    def recommend_tmdb_from_db(self, movie_title: str, number_of_movies: int = 5):
        result = self.data[self.data.title == movie_title][['recommendations', 'keywords', 'genres', 'overview']]

        recommendations = result['recommendations'].values[0]
        recommendations = pd.Series(eval(recommendations)) if isinstance(recommendations, str) else pd.Series(
            recommendations)
        recommendations = recommendations.iloc[:number_of_movies].values.tolist()

        results = []
        for title in recommendations:
            results.append([title,
                            self.data[self.data.title == title].popularity.values[0],
                            self.data[self.data.title == title].vote_average.values[0]])
        results = pd.DataFrame(results, columns=['title', 'popularity', 'vote_average'])
        return results

    def process_movie_title(self, movie_title):

        str2Match = movie_title
        strOptions = self.data.title.tolist()
        highest = process.extractOne(str2Match, strOptions)

        return highest[0]

    def find_posters_for_recommendations(self, results):
        df_urls = self.data.loc[self.data['title'].isin(results['title'])].loc[:, ['title', 'urls']]
        return pd.merge(results, df_urls, on='title')

    @classmethod
    def from_config_mongo(cls):
        with open(os.path.join(BASE_DIR, 'config.yaml')) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

            mongo_uri = data['MongoDB']['mongo_uri']

        try:
            conn = pymongo.MongoClient(mongo_uri)
            print("Connected successfully!!!")

            db = conn['tmdb_with_recom_scores_and_imdb_id']
            print("db self.conn succes")
            collection = db.records
            print("collection self.conn succes")
            df = pd.DataFrame(list(collection.find()))
            print("DF succes")
            return cls(df=df, conn=conn)

        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to MongoDB: %s" % e)

    @classmethod
    def from_csv(cls):
        path_csv = os.path.join(BASE_DIR, 'recommender/movies.csv')
        df = pd.read_csv(path_csv)
        return cls(df=df)


# USAGE
if __name__ == "__main__":
    # recommender = Recommender.from_config_mongo()
    recommender = Recommender.from_csv()
    # recommender.data.to_csv('movies.csv',index=False)
    print("juju")
    print(recommender.recommend('Harry Potter'))