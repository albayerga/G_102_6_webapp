import pandas as pd

from myapp.core.utils import load_tweet_id_mapping, load_docs
from myapp.search.objects import Document

_corpus = {}
tweet_id_to_doc_id = load_tweet_id_mapping()
doc_id_to_terms = load_docs()

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

    # add column terms and add terms to each tweet - get terms from the doc_id_to_terms dictionary
    data_tweets["Terms"] = data_tweets["Id"].map(doc_id_to_terms)

    # map the tweet id to the document id
    data_tweets["Id"] = data_tweets["Id"].map(tweet_id_to_doc_id)

    # get username from user -> username
    data_tweets["Username"] = data_tweets["user"].apply(lambda x: x["username"])

    columns = ['Id', 'Tweet', 'Date', 'Likes', 'Retweets', 'Url', 'Hashtags', 'Terms', 'Username'] # add terms if necessary
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
        row['Hashtags'],
        row['Terms'],
        row['Username']
    )