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
    └── problems/
```

## Build Phases

### Phase 1: Project Setup
- [x] Init git repo
- [x] Folder structure (`scrapers/`, `indexer/`, `rankers/`, `app/`, `data/`)
- [x] `requirements.txt` (flask, flask-wtf, selenium, webdriver-manager)
- [x] `.gitignore`
- [x] Package `__init__.py` files

### Phase 2: Data Scraping
- [x] LeetCode link scraper (`scrapers/lc_links.py`)
- [x] CodeForces link scraper (`scrapers/cf_links.py`)

### Phase 3: Content Extraction
- [ ] Crawl problem URLs, extract title + description
- [ ] Store in `data/problems/` with `data/index.json`

### Phase 4: Preprocessing
- [ ] Tokenizer, stopword removal, text cleaning
- [ ] Build vocab from corpus

### Phase 5: Indexing
- [ ] Inverted index with TF
- [ ] Document frequencies, IDF values
- [ ] Average document length
- [ ] Save indices as JSON

### Phase 6: TF-IDF Ranking
- [ ] Implement corrected TF-IDF scorer
- [ ] Fix multi-term scoring bug from original

### Phase 7: BM25 Ranking
- [ ] Implement BM25 scorer (same interface as TF-IDF)
- [ ] Tunable k1/b parameters

### Phase 8: Comparison Mode
- [ ] Side-by-side results for same query
- [ ] Rank change highlighting

### Phase 9: Flask API & Frontend
- [ ] Search form with algorithm toggle (TF-IDF / BM25 / Compare)
- [ ] JSON API
- [ ] Results UI with problem titles and scores

### Phase 10: Testing & Deployment
- [ ] Test queries, verify both rankers
- [ ] Deploy
