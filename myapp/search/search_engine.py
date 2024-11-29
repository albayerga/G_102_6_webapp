import random

from myapp.search.objects import ResultItem, Document
from myapp.search.algorithms import search_popularity


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
        results = build_results(corpus, search_id, search_query)

        return results
