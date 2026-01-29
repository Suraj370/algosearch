"""Fetch CodeForces problem list using the public REST API."""

import json
import requests

API_URL = "https://codeforces.com/api/problemset.problems"


def fetch_cf_problems(output_path="data/cf_links.txt",
                      index_path="data/cf_index.json"):
    """Fetch all CodeForces problems and save links + metadata."""
    resp = requests.get(API_URL)
    data = resp.json()

    if data["status"] != "OK":
        raise RuntimeError(f"API error: {data}")

    problems = data["result"]["problems"]
    print(f"Total problems on CodeForces: {len(problems)}")

    # build links and index
    entries = []
    for p in problems:
        contest_id = p.get("contestId")
        index = p.get("index")
        if not contest_id or not index:
            continue
        url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        entries.append({
            "contestId": contest_id,
            "index": index,
            "name": p.get("name", ""),
            "tags": p.get("tags", []),
            "url": url
        })

    # save links
    with open(output_path, "w") as f:
        for e in entries:
            f.write(e["url"] + "\n")

    # save index with metadata
    with open(index_path, "w") as f:
        json.dump(entries, f, indent=2)

    print(f"Saved {len(entries)} links to {output_path}")
    return entries


if __name__ == "__main__":
    fetch_cf_problems()
