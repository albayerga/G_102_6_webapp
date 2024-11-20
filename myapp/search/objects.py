import json


class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, tweet, date, likes, retweets, url, hashtags): # add terms if necessary
        self.id = id
        self.tweet = tweet
        self.date = date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags


    def to_json(self):
        return {
            "id": self.id,
            "tweet": self.tweet,
            "date": self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date),
            "likes": self.likes,
            "retweets": self.retweets,
            "url": self.url,
            "hashtags": self.hashtags,
        }

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, tweet, date, likes, retweets, url, hashtags):
        self.id = id
        self.tweet = tweet
        self.date = date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class ResultItem:
    def __init__(self, id, tweet, date, likes, retweets, url, hashtags, ranking):
        self.id = id
        self.tweet = tweet
        self.date = date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags
        self.ranking = ranking
