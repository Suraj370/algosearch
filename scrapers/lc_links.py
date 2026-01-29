"""Fetch LeetCode problem list using the public GraphQL API."""

import json
import time
import requests

GRAPHQL_URL = "https://leetcode.com/graphql"

LIST_QUERY = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: {}
  ) {
    total: totalNum
    questions: data {
      titleSlug
      title
      difficulty
      topicTags { name }
    }
  }
}
"""


def graphql_request(variables, max_retries=3):
    """Make a GraphQL request with retry logic."""
    for attempt in range(max_retries):
        resp = requests.post(GRAPHQL_URL, json={
            "query": LIST_QUERY,
            "variables": variables
        })
        if resp.status_code == 200:
            try:
                return resp.json()
            except requests.exceptions.JSONDecodeError:
                pass
        print(f"  Retry {attempt + 1}/{max_retries} (status {resp.status_code})")
        time.sleep(2 ** attempt)  # 1s, 2s, 4s backoff
    raise RuntimeError(f"Failed after {max_retries} retries")


def fetch_lc_problems(batch_size=50, output_path="data/lc_links.txt",
                      index_path="data/lc_index.json"):
    """Fetch all LeetCode problem slugs and save links + metadata."""
    # first call to get total count
    data = graphql_request({"categorySlug": "", "skip": 0, "limit": 1})
    total = data["data"]["problemsetQuestionList"]["total"]
    print(f"Total problems on LeetCode: {total}")

    all_problems = []
    for skip in range(0, total, batch_size):
        data = graphql_request(
            {"categorySlug": "", "skip": skip, "limit": batch_size}
        )
        questions = data["data"]["problemsetQuestionList"]["questions"]
        all_problems.extend(questions)
        print(f"Fetched {len(all_problems)}/{total}")
        time.sleep(0.5)

    # save links
    with open(output_path, "w") as f:
        for p in all_problems:
            f.write(f"https://leetcode.com/problems/{p['titleSlug']}/\n")

    # save index with metadata
    with open(index_path, "w") as f:
        json.dump(all_problems, f, indent=2)

    print(f"Saved {len(all_problems)} links to {output_path}")
    return all_problems


if __name__ == "__main__":
    fetch_lc_problems()
