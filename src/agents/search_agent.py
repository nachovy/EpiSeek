import asyncio
import requests

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_papers(query, top_k=5):
    """
    Search for scientific papers using Semantic Scholar API.
    Args:
        query (str): The search query.
        top_k (int): Number of papers to return.
    Returns:
        list: List of dictionaries containing paper details.
    """
    async def fetch():
        response = requests.get(SEMANTIC_SCHOLAR_API_URL, params={
            "query": query,
            "fields": "title,authors,year,abstract,externalIds",
            "limit": top_k
        })
        if response.status_code == 200:
            data = response.json().get("data", [])
            papers = []
            for paper in data:
                doi = paper.get("externalIds", {}).get("DOI", None)
                papers.append({
                    "title": paper.get("title", ""),
                    "authors": [author["name"] for author in paper.get("authors", [])],
                    "year": paper.get("year", ""),
                    "abstract": paper.get("abstract", ""),
                    "doi": doi,
                    "pdf_url": paper.get("openAccessPdf", {}).get("url", None)
                })
            return papers
        print(response.status_code, response.text)
        return []
    return asyncio.run(fetch())