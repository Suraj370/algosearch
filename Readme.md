# AlgoSearch

A search engine for programming problems (LeetCode / CodeForces) that supports both TF-IDF and BM25 ranking for side-by-side comparison.

## Project Structure

```
algosearch/
├── scrapers/          # Data collection from LeetCode & CodeForces
├── indexer/           # Preprocessing & index building
├── rankers/           # TF-IDF and BM25 scoring engines
├── app/               # Flask web app & UI
│   ├── templates/
│   └── static/
└── data/              # Scraped problem content & indices
```

## Build Phases

### Phase 1: Project Setup
- [x] Init git repo
- [x] Folder structure (`scrapers/`, `indexer/`, `rankers/`, `app/`, `data/`)
- [x] `requirements.txt` (flask, flask-wtf, selenium, webdriver-manager)
- [x] `.gitignore`
- [x] Package `__init__.py` files
- [x] Virtual environment (`venv/`)

**Tech stack:** Python 3, Flask, Selenium, webdriver-manager

### Phase 2: Data Scraping
- [x] LeetCode link scraper (`scrapers/lc_links.py`) — GraphQL API, 3,822 problems
- [x] CodeForces link scraper (`scrapers/cf_links.py`) — REST API, 10,967 problems

Both scrapers use public APIs (no Selenium needed) and fetch title, tags, and difficulty for each problem.

**Output files:**
| File | Contents |
|------|----------|
| `data/lc_links.txt` | LeetCode problem URLs |
| `data/lc_index.json` | LeetCode metadata (title, slug, difficulty, topicTags) |
| `data/cf_links.txt` | CodeForces problem URLs |
| `data/cf_index.json` | CodeForces metadata (name, contestId, index, tags) |

**Usage:**
```bash
python -m scrapers.lc_links
python -m scrapers.cf_links
```

### Phase 3: Preprocessing & Indexing (`indexer/preprocess.py`)
- [x] Tokenizer, stopword removal, text cleaning
- [x] Build vocab from corpus (7,537 unique terms)
- [x] Inverted index with TF
- [x] Document frequencies, IDF values
- [x] Average document length (6.8 tokens)
- [x] Save all indices as JSON

Loads both `lc_index.json` (3,822 problems) and `cf_index.json` (10,967 problems) into a unified corpus of **14,789 documents**. Tokenizes each problem's title + tags — lowercase, strip non-alphanumeric, remove stopwords.

**Output files:**
| File | Contents |
|------|----------|
| `data/corpus.json` | All docs with tokens, title, URL, source |
| `data/vocab.json` | 7,537 unique terms with document frequency |
| `data/inverted_index.json` | term → list of `{doc_id, tf}` |
| `data/idf.json` | Precomputed IDF per term |
| `data/meta.json` | Total docs (14,789), avg doc length (6.8), vocab size |

**Usage:**
```bash
python -m indexer.preprocess
```

### Phase 4: Ranking Engines (`rankers/tfidf.py`, `rankers/bm25.py`)
- [x] TF-IDF scorer — `TF = count / doc_length`, `IDF = log((1+N) / (1+df))`, sum across query terms
- [x] BM25 scorer — `IDF * (tf * (k1+1)) / (tf + k1 * (1 - b + b * (dl/avgdl)))`, tunable `k1=1.5`, `b=0.75`
- [x] Both share the same `rank(query_terms, top_k)` interface

Both rankers load the precomputed index at init and return ranked results with score, title, URL, and source.

**Key difference:** For query "binary tree", TF-IDF ranks short CodeForces problems with just "Tree" at #4-6 (inflated TF from short doc length). BM25 correctly surfaces "Binary Search Tree" problems instead due to term frequency saturation and relative length normalization.

**Usage:**
```bash
python -m rankers.tfidf
python -m rankers.bm25
```

### Phase 5: Flask API, Frontend & Comparison Mode (`app/app.py`)
- [x] Search form with algorithm toggle (TF-IDF / BM25 / Compare)
- [x] JSON API
- [x] Results UI with problem titles and scores
- [x] Side-by-side comparison view with rank change highlighting

Flask web app with two routes:

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET/POST | Search form with algorithm dropdown (TF-IDF, BM25, Compare) |
| `/api/search?q=...&method=tfidf\|bm25\|compare` | GET | JSON API for programmatic access |

**Compare mode** runs both rankers on the same query and displays results in a two-column layout. Each BM25 result shows its TF-IDF rank when different, highlighting where the algorithms disagree.

**Files:**
| File | Purpose |
|------|---------|
| `app/app.py` | Flask routes, form handling, ranker integration |
| `app/templates/index.html` | Search UI with single/compare result views |
| `app/static/style.css` | Dark theme, responsive layout, source badges |

**Usage:**
```bash
python app/app.py
# Open http://127.0.0.1:5000
```

### Phase 6: Testing & Deployment
- [ ] Test queries, verify both rankers
- [ ] Deploy
