import collections
import numpy as np
from numpy import linalg as la

from myapp.core.utils import build_terms, load_tweets_popularity, load_tf, load_idf, load_index

# Load the inverted index, idf and tf from the disk


def search_in_corpus(query):
    # 1. create create_tfidf_index

    # 2. apply ranking
    return ""


# load index, idf, tf and tweets_popularity from disk (computed in previous labs)
index = load_index()
idf = load_idf()
tf = load_tf()
tweets_popularity = load_tweets_popularity()


def rank_documents_popularity(terms, docs):
    
    doc_vectors = collections.defaultdict(lambda: [0] * len(terms))
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms) 

    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):
        if term not in index:
            continue

        query_vector[termIndex] = query_terms_count[term] / query_norm * idf[term]

        # generate doc_vectors for matching docs
        for doc_index, (doc, doc_positions) in enumerate(index[term]):
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]

    doc_scores = []

    for doc, curDocVec in doc_vectors.items():

        popularity_score = tweets_popularity[doc]
        cosine_similarity = np.dot(curDocVec, query_vector)
        combined_score = 0.6 * cosine_similarity + 0.4 * popularity_score

        doc_scores.append([combined_score, doc])

    doc_scores.sort(reverse=True) # sort by score
    result_docs = [x[1] for x in doc_scores] # get the doc ids

    if len(result_docs) == 0:
        print("No results found, try again")
        query = input()
        docs = search_popularity(query)

    return result_docs


def search_popularity(query):

    terms = build_terms(query,'english') # get the terms from the query
    docs = set()

    i=0
    for term in terms:
        try:
            # store in term_docs the ids of the docs that contain "term"
            term_docs = [posting[0] for posting in index[term]]

            if i == 0:
                docs = set(term_docs)
                i = 1

            else: docs &= set(term_docs)

        except:
            #term is not in index
            pass

    docs = list(docs)
    ranked_docs = rank_documents_popularity(terms, docs)

    return ranked_docs