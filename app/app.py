"""Flask web app for AlgoSearch — search with TF-IDF, BM25, or compare both."""

import sys
import os

# ensure project root is on sys.path so rankers/ can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField

from rankers.tfidf import TFIDFRanker
from rankers.bm25 import BM25Ranker

app = Flask(__name__)
app.config["SECRET_KEY"] = "algosearch-dev-key"

# load rankers once at startup
tfidf_ranker = TFIDFRanker()
bm25_ranker = BM25Ranker()


class SearchForm(FlaskForm):
    search = StringField("Search")
    method = SelectField("Algorithm", choices=[
        ("tfidf", "TF-IDF"),
        ("bm25", "BM25"),
        ("compare", "Compare"),
    ])
    submit = SubmitField("Search")


@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    results = None
    query = ""
    method = "tfidf"

    if form.validate_on_submit():
        query = form.search.data.strip()
        method = form.method.data
        q_terms = [t.lower() for t in query.split() if t]

        if q_terms:
            if method == "tfidf":
                results = {"tfidf": tfidf_ranker.rank(q_terms)}
            elif method == "bm25":
                results = {"bm25": bm25_ranker.rank(q_terms)}
            else:  # compare
                results = {
                    "tfidf": tfidf_ranker.rank(q_terms),
                    "bm25": bm25_ranker.rank(q_terms),
                }

    return render_template("index.html", form=form, results=results,
                           query=query, method=method)


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    method = request.args.get("method", "bm25")
    top_k = int(request.args.get("top_k", 20))

    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    q_terms = [t.lower() for t in query.split() if t]

    if method == "tfidf":
        return jsonify({"method": "tfidf", "results": tfidf_ranker.rank(q_terms, top_k)})
    elif method == "bm25":
        return jsonify({"method": "bm25", "results": bm25_ranker.rank(q_terms, top_k)})
    elif method == "compare":
        return jsonify({
            "tfidf": tfidf_ranker.rank(q_terms, top_k),
            "bm25": bm25_ranker.rank(q_terms, top_k),
        })
    else:
        return jsonify({"error": f"Unknown method: {method}"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
