"""TF-IDF ranker. Scores documents against a query using TF-IDF.

TF  = term_count / doc_length
IDF = log((1 + N) / (1 + df))
Score = sum of (TF * IDF) across all query terms
"""

import json
import math


class TFIDFRanker:
    def __init__(self, data_dir="data"):
        with open(f"{data_dir}/corpus.json", "r") as f:
            self.corpus = json.load(f)
        with open(f"{data_dir}/inverted_index.json", "r") as f:
            self.inverted_index = json.load(f)
        with open(f"{data_dir}/idf.json", "r") as f:
            self.idf = json.load(f)
        with open(f"{data_dir}/meta.json", "r") as f:
            self.meta = json.load(f)

    def rank(self, query_terms, top_k=20):
        """Rank documents by TF-IDF score for the given query terms.

        Returns list of (doc_id, score, title, url, source).
        """
        scores = {}

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            idf_value = self.idf.get(term, 0)

            for entry in self.inverted_index[term]:
                doc_id = entry["doc"]
                tf_raw = entry["tf"]
                doc_len = self.corpus[doc_id]["length"]

                if doc_len == 0:
                    continue

                tf = tf_raw / doc_len
                tf_idf = tf * idf_value

                scores[doc_id] = scores.get(doc_id, 0) + tf_idf

        # sort by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in ranked[:top_k]:
            doc = self.corpus[doc_id]
            results.append({
                "doc_id": doc_id,
                "score": round(score, 6),
                "title": doc["title"],
                "url": doc["url"],
                "source": doc["source"],
            })

        return results


if __name__ == "__main__":
    ranker = TFIDFRanker()
    query = input("Enter search query: ").lower().split()
    results = ranker.rank(query)
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['source']}] {r['title']} (score: {r['score']})")
        print(f"   {r['url']}")
