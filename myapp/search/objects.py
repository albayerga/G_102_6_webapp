import json


class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, tweet, date, likes, retweets, url, hashtags, username):
        self.id = id
        self.tweet = tweet
        self.date = date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags
        self.username = username


    def to_json(self):
        return {
            "id": self.id,
            "tweet": self.tweet,
            "date": self.date.isoformat() if hasattr(self.date, 'isoformat') else str(self.date),
            "likes": self.likes,
            "retweets": self.retweets,
            "url": self.url,
            "hashtags": self.hashtags,
            "username": self.username,
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
    def __init__(self, id, tweet, date, likes, retweets, url, hashtags, username, ranking):
        self.id = id
        self.tweet = tweet
        self.date = date
        self.likes = likes
        self.retweets = retweets
        self.url = url # this is the url to the details page -> format: "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id)
        self.hashtags = hashtags
        self.username = username
        self.ranking = ranking
