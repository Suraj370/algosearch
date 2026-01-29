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

### Phase 4: TF-IDF Ranking
- [ ] Implement corrected TF-IDF scorer
- [ ] Fix multi-term scoring bug from original

### Phase 5: BM25 Ranking
- [ ] Implement BM25 scorer (same interface as TF-IDF)
- [ ] Tunable k1/b parameters

### Phase 6: Comparison Mode
- [ ] Side-by-side results for same query
- [ ] Rank change highlighting

### Phase 7: Flask API & Frontend
- [ ] Search form with algorithm toggle (TF-IDF / BM25 / Compare)
- [ ] JSON API
- [ ] Results UI with problem titles and scores

### Phase 8: Testing & Deployment
- [ ] Test queries, verify both rankers
- [ ] Deploy
