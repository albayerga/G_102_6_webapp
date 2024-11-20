import pandas as pd

from myapp.core.utils import build_terms, load_tweet_id_mapping, build_terms
from myapp.search.objects import Document

_corpus = {}
tweet_id_to_doc_id = load_tweet_id_mapping()

def load_corpus(path) -> [Document]:
    """
    Load file and transform to dictionary with each document as an object for easier treatment when needed for displaying
     in results, stats, etc.
    :param path:
    :return:
    """
    df = _load_corpus_as_dataframe(path)
    df.apply(_row_to_doc_dict, axis=1)

    return _corpus


def _load_corpus_as_dataframe(path):
    """
    Load documents corpus from file in 'path'
    Return a DataFrame with the corpus content
    """

    original_data_tweets = pd.read_json(path, lines=True, compression="gzip")
    data_tweets = original_data_tweets.copy()
    data_tweets.rename(columns={
        'id': 'Id',
        'content': 'Tweet',
        'date': 'Date',
        'likeCount': 'Likes',
        'retweetCount': 'Retweets',
        'url': 'Url',
    }, inplace=True)
    data_tweets['Hashtags'] = data_tweets['Tweet'].apply(lambda x: [i for i in x.split() if i.startswith("#")]) # add a column for hashtags

    # add column terms and apply build_terms function to each row Tweet
    # data_tweets['Terms'] = data_tweets['Tweet'].apply(lambda x: build_terms(x, 'english'))

    # map the tweet id to the document id
    data_tweets["Id"] = data_tweets["Id"].map(tweet_id_to_doc_id)

    columns = ['Id', 'Tweet', 'Date', 'Likes', 'Retweets', 'Url', 'Hashtags'] # add terms if necessary
    return data_tweets[columns]


def _row_to_doc_dict(row: pd.Series):
    # Add the document to the corpus dictionary
    _corpus[row['Id']] = Document(
        row['Id'], 
        row['Tweet'][0:100],  # Tweet truncated to first 100 characters - we won't need to show the whole tweet if too long
        row['Date'], 
        row['Likes'], 
        row['Retweets'], 
        row['Url'], 
        row['Hashtags']
        # row['Terms']  # add it if necessary
    )