"""BM25 ranker. Scores documents against a query using Okapi BM25.

Score = IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (dl / avgdl)))

k1 controls term frequency saturation (default 1.5)
b  controls length normalization (default 0.75)
"""

import json
import math


class BM25Ranker:
    def __init__(self, data_dir="data", k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b

        with open(f"{data_dir}/corpus.json", "r") as f:
            self.corpus = json.load(f)
        with open(f"{data_dir}/inverted_index.json", "r") as f:
            self.inverted_index = json.load(f)
        with open(f"{data_dir}/idf.json", "r") as f:
            self.idf = json.load(f)
        with open(f"{data_dir}/meta.json", "r") as f:
            self.meta = json.load(f)

        self.avgdl = self.meta["avg_dl"]

    def rank(self, query_terms, top_k=20):
        """Rank documents by BM25 score for the given query terms.

        Returns list of (doc_id, score, title, url, source).
        """
        scores = {}

        for term in query_terms:
            if term not in self.inverted_index:
                continue

            idf_value = self.idf.get(term, 0)

            for entry in self.inverted_index[term]:
                doc_id = entry["doc"]
                tf = entry["tf"]
                dl = self.corpus[doc_id]["length"]

                # BM25 formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (dl / self.avgdl))
                bm25_score = idf_value * (numerator / denominator)

                scores[doc_id] = scores.get(doc_id, 0) + bm25_score

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
    ranker = BM25Ranker()
    query = input("Enter search query: ").lower().split()
    results = ranker.rank(query)
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['source']}] {r['title']} (score: {r['score']})")
        print(f"   {r['url']}")
