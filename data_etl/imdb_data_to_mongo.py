import os
import pandas as pd
import pymongo


def imdb_to_mongo(local=False):
    # data_folder = '../data'

    # The dataset files can be accessed and downloaded from https://datasets.imdbws.com/
    # files = os.listdir(data_folder)
    # files = [os.path.join(data_folder, f) for f in files]

    ratings = pd.read_csv('/home/aitor/Escritorio/Msc Data Science/ADS/Project/Imdb/title.ratings.tsv', sep="\t")
    basics = pd.read_csv('/home/aitor/Escritorio/Msc Data Science/ADS/Project/Imdb/title.basics.tsv', sep="\t")

    basics = pd.concat([basics, ratings], axis=1, join='inner')
    df = basics[basics["endYear"] != "\\N"]

    to_drop = ['tconst', 'titleType', 'originalTitle', 'isAdult', 'endYear', 'runtimeMinutes']
    df.drop(to_drop, axis=1, inplace=True)
    df.dropna(axis=0, how='any', inplace=True)
    df.rename(columns={'primaryTitle': 'title', 'startYear': 'release_year',
                       'averageRating': 'vote_average', 'numVotes': 'vote_count'}, inplace=True)

    if local:
        # For local version of db
        df.to_csv('merged.csv')
    else:
        mongo_uri = "mongodb+srv://test:1234@cluster0.rvcwr.mongodb.net/imdbADS?retryWrites=true&w=majority"

        # Connect to MongoDB
        try:
            conn = pymongo.MongoClient(mongo_uri)
            print("Connected successfully!!!")

        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to MongoDB: %s" % e)

        db = conn['imdbADS']
        collection = db.preprocessed_data
        collection.insert_many(df.to_dict("records"))


imdb_to_mongo()
