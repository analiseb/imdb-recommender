import pandas as pd
import pymongo
from ast import literal_eval
import numpy as np


def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        # Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    # Return empty list in case of missing/malformed data
    return []


movies = pd.read_csv("/home/aitor/Escritorio/movies_metadata.csv",
                     usecols=["id", "title", "genres", "overview", "popularity", "vote_average"])

movies['genres'] = movies['genres'].fillna('[]').apply(literal_eval). \
    apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

keywords = pd.read_csv("/home/aitor/Escritorio/keywords.csv", usecols=["id", "keywords"])
keywords["keywords"] = keywords["keywords"].apply(literal_eval)
keywords["keywords"] = keywords["keywords"].apply(get_list)


movies = pd.merge(movies, keywords, left_index=True, right_index=True)
movies.rename(columns={'id_x': 'id'}, inplace=True)
movies.drop(columns=['id_y'], inplace=True)


mongo_uri = "mongodb+srv://test:1234@cluster0.rvcwr.mongodb.net/imdbADS?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    conn = pymongo.MongoClient(mongo_uri)
    print("Connected successfully!!!")

except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: %s" % e)

db = conn['tmdbADS']
collection = db.tmdb_v2
collection.insert_many(movies.to_dict("records"))
