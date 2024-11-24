import random

from myapp.search.objects import ResultItem, Document
from myapp.search.algorithms import search_popularity


def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        # res.append(ResultItem(item.id, item.tweet, item.likes, item.date,
        #                       "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))
        res.append(ResultItem(item.id, item.tweet, item.date, item.likes, item.retweets, item.url, item.hashtags, item.username, random.random()))

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res

def build_results(corpus: dict, search_id, search_query):
    res = []
    result = search_popularity(search_query)

    # maybe we should add a max number of results to show !!!

    for idx in range(len(result)):
        doc_id = result[idx]
        # ranking is the index in the list because the result from search_popularity is already sorted
        item: Document = corpus[doc_id]
        format_url = "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id)
        res.append(ResultItem(item.id, item.tweet, item.date, item.likes, item.retweets, format_url, item.hashtags, item.username, idx))
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res

    


class SearchEngine:
    """educational search engine"""

    def search(self, search_query, search_id, corpus):
        print("Search query:", search_query)

        results = []
        ##### your code here #####
        #results = build_demo_results(corpus, search_id)  # replace with call to search algorithm
        results = build_results(corpus, search_id, search_query)
        # results = search_in_corpus(search_query)
        ##### your code here #####

        return results
