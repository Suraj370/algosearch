"""Preprocessing pipeline: load raw problem data, tokenize, remove stopwords,
build vocab, inverted index, IDF values, and document metadata.

Reads from data/lc_index.json and data/cf_index.json.
Writes to data/corpus.json, data/vocab.json, data/inverted_index.json.
"""

import json
import math
import os
import re

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "dare",
    "it", "its", "this", "that", "these", "those", "i", "you", "he", "she",
    "we", "they", "me", "him", "her", "us", "them", "my", "your", "his",
    "our", "their", "what", "which", "who", "whom", "where", "when", "how",
    "not", "no", "nor", "as", "if", "then", "than", "so", "such", "both",
    "each", "all", "any", "few", "more", "most", "other", "some", "only",
    "same", "too", "very", "just", "about", "above", "after", "before",
    "between", "into", "through", "during", "out", "up", "down", "over",
    "under", "again", "further", "once", "here", "there", "also",
}


def tokenize(text):
    """Lowercase, strip non-alphanumeric, split into tokens, remove stopwords."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    tokens = text.split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def build_document_text(problem, source):
    """Build a searchable text string from a problem's metadata."""
    parts = []

    if source == "lc":
        parts.append(problem.get("title", ""))
        tags = problem.get("topicTags", [])
        parts.extend(tag["name"] for tag in tags)
        parts.append(problem.get("difficulty", ""))
    elif source == "cf":
        parts.append(problem.get("name", ""))
        parts.extend(problem.get("tags", []))

    return " ".join(parts)


def load_problems(data_dir="data"):
    """Load LC and CF problems into a unified list."""
    documents = []

    # LeetCode
    lc_path = os.path.join(data_dir, "lc_index.json")
    if os.path.exists(lc_path):
        with open(lc_path, "r", encoding="utf-8") as f:
            lc_problems = json.load(f)
        for p in lc_problems:
            text = build_document_text(p, "lc")
            url = f"https://leetcode.com/problems/{p['titleSlug']}/"
            documents.append({
                "title": p.get("title", ""),
                "url": url,
                "source": "leetcode",
                "raw_text": text,
            })

    # CodeForces
    cf_path = os.path.join(data_dir, "cf_index.json")
    if os.path.exists(cf_path):
        with open(cf_path, "r", encoding="utf-8") as f:
            cf_problems = json.load(f)
        for p in cf_problems:
            text = build_document_text(p, "cf")
            documents.append({
                "title": p.get("name", ""),
                "url": p.get("url", ""),
                "source": "codeforces",
                "raw_text": text,
            })

    return documents


def build_index(data_dir="data", output_dir="data"):
    """Full preprocessing pipeline: tokenize, build vocab & inverted index."""
    print("Loading problems...")
    documents = load_problems(data_dir)
    print(f"Loaded {len(documents)} documents")

    # tokenize all documents
    corpus = []
    for doc in documents:
        tokens = tokenize(doc["raw_text"])
        corpus.append({
            "title": doc["title"],
            "url": doc["url"],
            "source": doc["source"],
            "tokens": tokens,
            "length": len(tokens),
        })

    # build vocab (term -> document frequency)
    vocab = {}
    for doc_id, doc in enumerate(corpus):
        seen_terms = set(doc["tokens"])
        for term in seen_terms:
            if term not in vocab:
                vocab[term] = 0
            vocab[term] += 1

    # build inverted index: term -> list of (doc_id, term_frequency)
    inverted_index = {}
    for doc_id, doc in enumerate(corpus):
        tf_counts = {}
        for token in doc["tokens"]:
            tf_counts[token] = tf_counts.get(token, 0) + 1
        for term, count in tf_counts.items():
            if term not in inverted_index:
                inverted_index[term] = []
            inverted_index[term].append({"doc": doc_id, "tf": count})

    # compute IDF values
    n = len(corpus)
    idf = {}
    for term, df in vocab.items():
        idf[term] = math.log((1 + n) / (1 + df))

    # average document length (for BM25)
    total_tokens = sum(doc["length"] for doc in corpus)
    avg_dl = total_tokens / n if n > 0 else 0

    # save everything
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "corpus.json"), "w") as f:
        json.dump(corpus, f)

    with open(os.path.join(output_dir, "vocab.json"), "w") as f:
        json.dump(vocab, f)

    with open(os.path.join(output_dir, "inverted_index.json"), "w") as f:
        json.dump(inverted_index, f)

    with open(os.path.join(output_dir, "idf.json"), "w") as f:
        json.dump(idf, f)

    with open(os.path.join(output_dir, "meta.json"), "w") as f:
        json.dump({"total_docs": n, "avg_dl": avg_dl, "vocab_size": len(vocab)}, f, indent=2)

    print(f"Vocab size: {len(vocab)}")
    print(f"Avg doc length: {avg_dl:.1f} tokens")
    print(f"Index saved to {output_dir}/")

    return corpus, vocab, inverted_index, idf


if __name__ == "__main__":
    build_index()
