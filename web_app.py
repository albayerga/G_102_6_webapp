import os
from json import JSONEncoder

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session, jsonify, request

from myapp.analytics.analytics_data import AnalyticsData
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()

# instantiate our in memory persistence
analytics_data = AnalyticsData()

# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path = path + "/data/farmers-protest-tweets.json.gz" # path to the corpus file
print("loading corpus from file:", file_path)

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path)
# print("loaded corpus. first elem:", list(corpus.values())[0])


# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2021 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():

    search_query = request.form['search-query']
    session['last_search_query'] = search_query
    user_agent = request.headers.get('User-Agent')
    user_ip = request.remote_addr
    search_id = analytics_data.save_query_terms(search_query, user_agent, user_ip)
    results = search_engine.search(search_query, search_id, corpus)

    found_count = len(results)
    session['last_found_count'] = found_count

    analytics_data.track_visitor(user_agent, user_ip)

    print(session)
    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count)


@app.route('/doc_details', methods=['GET'])
def doc_details():
    clicked_doc_id = request.args["id"]
    search_id = int(request.args["search_id"])
    analytics_data.track_click(clicked_doc_id, search_id)

    # Actualiza el dwell time al regresar
    analytics_data.track_return(clicked_doc_id)

    # Obtén el documento del corpus
    doc = corpus[clicked_doc_id]
    return render_template('doc_details.html', doc=doc, page_title="Document Details")

@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """
    docs = []
    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[doc_id]
        count = len(analytics_data.fact_clicks[doc_id])
        #count = analytics_data.fact_clicks[doc_id]
        docs.append({"id": row.id, "tweet": row.tweet, "count": count})
        #doc = StatsDocument(row.id, row.tweet, row.date, row.url, count)
        #docs.append(doc)

    # simulate sort by ranking
    docs.sort(key=lambda doc: doc["count"], reverse=True)


    query_stats = len(analytics_data.fact_queries)
    click_stats = sum(len(v) for v in analytics_data.fact_clicks.values())
    visited_docs = []
    for doc_id, queries in analytics_data.fact_clicks.items():
        row = corpus[doc_id]
        counter = len(queries)
        visited_docs.append({
            "doc_id": doc_id,
            "description": row.tweet,
            "counter": counter
        })

    # Ordenar por el número de visitas (descendente)
    visited_docs.sort(key=lambda doc: doc["counter"], reverse=True)
    
    return render_template('stats.html', 
                           clicks_data=docs,
                           query_stats=query_stats, 
                           click_stats=click_stats, 
                           visited_docs=visited_docs)


@app.route('/dashboard', methods=['GET'])
def dashboard():

    visited_docs = []
    for doc_id, queries in analytics_data.fact_clicks.items():
        row = corpus[doc_id]
        counter = len(queries)
        visited_docs.append({
            "doc_id": doc_id,
            "description": row.tweet,
            "counter": counter
        })

    # Ordenar por el número de visitas (descendente)
    visited_docs.sort(key=lambda doc: doc["counter"], reverse=True)

    query_stats = len(analytics_data.fact_queries)
    visitor_stats = len(set(v['ip'] for v in analytics_data.fact_visitors))
    click_stats = sum(len(v) for v in analytics_data.fact_clicks.values())
    session_stats = len(analytics_data.fact_sessions)
    avg_dwell_time = _calculate_avg_dwell_time()

    clicks_by_doc = [
        {"doc_id": doc_id, "clicks": len(queries)}
        for doc_id, queries in analytics_data.fact_clicks.items()
    ]
    clicks_by_doc.sort(key=lambda x: x["clicks"], reverse=True)

    return render_template('dashboard.html', 
                           visited_docs=visited_docs,
                           query_stats=query_stats,
                           visitor_stats=visitor_stats,
                           click_stats=click_stats,
                           session_stats=session_stats,
                           avg_dwell_time=avg_dwell_time,
                           clicks_by_doc=clicks_by_doc) #

# Endpoint para datos de sesiones
@app.route('/api/sessions', methods=['GET'])
def api_sessions():
    sessions = [
        {
            "session_id": session_id,
            "queries": len(data["queries"]),
            "clicks": len(data["clicks"]),
            "start_time": data["start_time"].isoformat()
        }
        for session_id, data in analytics_data.fact_sessions.items()
    ]
    return jsonify(sessions)

# Endpoint para dwell time
@app.route('/api/dwell-time', methods=['GET'])
def api_dwell_time():
    dwell_times = [
        {"doc_id": doc_id, "dwell_time": click["dwell_time"]}
        for doc_id, clicks in analytics_data.fact_clicks.items()
        for click in clicks if click["dwell_time"] is not None
    ]
    return jsonify(dwell_times)

def _calculate_avg_dwell_time():
    total_time = 0
    count = 0
    for clicks in analytics_data.fact_clicks.values():
        for click in clicks:
            if click["dwell_time"] is not None:
                total_time += click["dwell_time"]
                count += 1
    return total_time / count if count > 0 else 0

@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
