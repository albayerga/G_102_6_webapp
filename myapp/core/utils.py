import datetime
import os
from random import random
import re
import pickle

import string
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from faker import Faker
import pandas as pd

fake = Faker()

# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


def build_terms(line, lang):

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words(lang)) # get the stop words for the language

    line = re.sub(r'http\S+', '', line)
    words_line= line.split() # tokenize the text, get a list of terms

    #First we deal with # separation
    treated_words = []
    for word in words_line:

        if word and word[0] == "#":  #If its a hashtag
            separated_list = re.split(r'(?<=[a-z])(?=[A-Z])', word[1:])
            for separated_word in separated_list:
                treated_words.append(separated_word)
        else:
            treated_words.append(word)


    line = [word.lower() for word in treated_words] # everything to lowercase
    translator = str.maketrans('', '', string.punctuation)
    line = [word.translate(translator) for word in line]  # remove punctuation

    line= [word for word in line if word not in stop_words] # remove stop_words
    line= [stemmer.stem(word) for word in line ] # steam
    line = [word for word in line if word.isalnum()]  # keeps only words with alphanumeric characters

    return line


def load_tweet_id_mapping():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/tweet_document_ids_map.csv")
    file_path = os.path.normpath(file_path)
    
    # Read the file once
    tweet_document_ids_map = pd.read_csv(file_path)
    
    # Convert it to a dictionary for faster lookups
    return dict(zip(tweet_document_ids_map["id"], tweet_document_ids_map["docId"]))


# docs is a dictionary with doc_id as key and the "terms" of each doc as value
def load_docs():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/docs.pkl")
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'rb') as f:
        docs = pickle.load(f)
    
    return docs


# tweets_popularity is a dictionary with doc_id as key and the popularity score of each doc as value
def load_tweets_popularity():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/tweets_popularity.pkl")
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'rb') as f:
        tweets_popularity = pickle.load(f)
    
    return tweets_popularity

# ---------------------------------------------------

def load_df():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/df.pkl")
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'rb') as f:
        df = pickle.load(f)
    
    return df


def load_tf():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/tf.pkl")
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'rb') as f:
        tf = pickle.load(f)
    
    return tf


def load_idf():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/idf.pkl")
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'rb') as f:
        idf = pickle.load(f)
    
    return idf


# index is a dictionary with term as key and a list of doc_id with their positions as value
def load_index():
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    file_path = os.path.join(path, "../../data/index.pkl")
    file_path = os.path.normpath(file_path)
    
    with open(file_path, 'rb') as f:
        index = pickle.load(f)
    
    return index