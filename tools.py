from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def searcher(query:str)->str:
    '''Search the web for recent and reliable information on a topic. Return titles, URLs and snippets. After every search, provide the URLs for results'''
    results=tavily.search(query=query,max_results=3)

    out=[]

    for r in results['results']:
        out.append(
            f'Title:{r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}'
        )

    return "\n----\n".join(out)

@tool
def scrape_web(url: str) -> str:
    '''Get the text content of a webpage from its URL.'''
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        html = requests.get(url, headers=headers, timeout=8).text
    except Exception as e:
        return f"Error: {e}"

    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)[:1800]
