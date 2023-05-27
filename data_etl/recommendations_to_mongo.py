import os
import pandas as pd
import pymongo
import numpy as np
import pickle
from bson.binary import Binary
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def recommendations_to_mongo():

    mongo_uri = "mongodb+srv://test:1234@cluster0.rvcwr.mongodb.net/imdbADS?retryWrites=true&w=majority"

    # Connect to MongoDB
    try:
        conn = pymongo.MongoClient(mongo_uri)
        print("Connected successfully!!!")

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)

    db = conn['tmdbADS']
    collection = db.tmdb_v2
    data = pd.DataFrame(list(collection.find()))

    # dataframe preprocessing
    data = data.dropna()
    data = data.drop_duplicates(subset=['title'])
    # data = data[pd.to_numeric(data.popularity, errors='coerce')]
    data = data.reset_index(drop=True)

    # overviews NLP preprocessing
    tfidf = TfidfVectorizer(stop_words='english')

    data['overview'] = data['overview'].str.lower()
    data['overview'] = data['overview'].fillna('')

    tfidf_matrix = tfidf.fit_transform(data['overview'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    number_of_movies = 10
    recommendations = []
    # sim_scores_all = []
    indices = pd.Series(data.index, index=data['title']).drop_duplicates()

    for i, movie_title in enumerate(data.title.tolist()):
        idx = indices[movie_title]

        print(f'{i} / {data.shape[0]}')

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:number_of_movies+1]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        recommendations.append([movie_title, data['title'].iloc[movie_indices].tolist(), sim_scores])
        # sim_scores_all.append(sim_scores)

    recommendations = pd.DataFrame(recommendations, columns=['title', 'recommendations', 'scores'])

    data = pd.merge(data, recommendations, how='inner', on='title',
                        # left_on=None, right_on=None
                        )


    db = conn['tmdb_with_recom_and_scores_expanded']
    collection = db['records']
    collection.insert_many(data.to_dict("records"))


recommendations_to_mongo()
