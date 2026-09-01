from urllib.parse import urlparse

from tavily import TavilyClient

from app.config import TAVILY_API_KEY


client = TavilyClient(api_key=TAVILY_API_KEY)

TRUSTED_DOMAINS = {
    "fda.gov" : 1,
    "efsa.europa.eu" : 1,
    "who.init" : 1,
    "nih.gov" : 1,
    "pubmed.ncbi.nlm.nih.gov" : 1,
    "openfoodfacts.org" : 2
}

def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www", "")

def search_ingredient(name: str):
    query = f'"{name}" food additive safety uses FDA EFSA'

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=8
    )

    results = []

    for result in response.get("results", []):

        url = result.get("url", "")
        domain = get_domain(url)

        if domain == "quora.com":
            continue

        source_tier = TRUSTED_DOMAINS.get(domain, 3)

        results.append(
            {
                "title": result.get("title"),
                "url": url,
                "domain": domain,
                "content": result.get("content"),
                "score": result.get("score"),
                "source_tier": source_tier
            }
        )

    results.sort(
        key=lambda item: (
            item["source_tier"],
            -(item["score"] or 0)
        )
    )

    return results