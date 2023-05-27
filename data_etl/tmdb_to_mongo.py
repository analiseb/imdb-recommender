import pymongo
import pandas as pd


def tmbd_to_mongo(local=False):
    df = pd.read_csv("/home/aitor/Escritorio/moviesTMDB2020.csv")
    df.drop(["poster_path"], axis=1, inplace=True)
    df['genre'] = df['genre'].str.replace(" ", ",").str[0:-1]
    df.dropna(subset=['overview'], inplace=True)

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

        db = conn['tmdbADS']
        collection = db.tmdb
        collection.insert_many(df.to_dict("records"))


tmbd_to_mongo()
