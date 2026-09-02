#!/usr/bin/env python3
"""Parse allunity.ru and generate REAL_CONTENT for migrate_data.py."""
import requests
from bs4 import BeautifulSoup
import json
import re

BASE = "https://allunity.ru"


def fetch(path):
    url = f"{BASE}/{path}"
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    return BeautifulSoup(r.text, "html.parser")


def extract_journal():
    soup = fetch("journal.shtml")
    articles = []
    for art in soup.select("article")[:5]:
        title = art.find("h3") or art.find("a")
        authors = art.find(class_=re.compile("author", re.I))
        abstract = art.find("p")
        link = art.find("a", href=True)
        articles.append({
            "title": title.get_text(strip=True) if title else "",
            "authors": authors.get_text(strip=True) if authors else "",
            "abstract": abstract.get_text(strip=True) if abstract else "",
            "url": BASE + link["href"] if link and link.get("href") else BASE + "/journal.shtml",
        })
    return {
        "title": "Журнал «Интегральная филосоефия»",
        "volume": "№ 15",
        "description": "<p>Научный журнал «Интегральная философия» — электронное периодическое издание, посвящённое философии всеединства.</p>",
        "articles": [{"type": "article", "value": a} for a in articles],
    }


def extract_library():
    soup = fetch("library.shtml")
    resources = []
    for item in soup.select("article a, .card a")[:5]:
        resources.append({
            "title": item.get_text(strip=True),
            "author": "AllUnity",
            "resource_type": "Книга",
            "url": item.get("href", BASE + "/library.shtml"),
            "description": "<p>Ресурс по интегральной философии.</p>",
        })
    return {
        "title": "Библиотека",
        "description": "<p>Ресурсы по интегральной философии и смежным областям.</p>",
        "resources": [{"type": "resource", "value": r} for r in resources],
    }


def extract_journal_full():
    """Get all journal articles."""
    soup = fetch("journal.shtml")
    articles = []
    seen_urls = set()
    
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "journal" in href and href.endswith(".shtml") and href not in seen_urls:
            seen_urls.add(href)
            try:
                detail = fetch(href.replace("index.shtml", "").strip("/") or "journal.shtml")
                title = detail.find("h1") or link
                authors_elem = detail.find(class_=re.compile("author|authors", re.I))
                p = detail.find("p")
                articles.append({
                    "title": title.get_text(strip=True) if title else "Без названия",
                    "authors": authors_elem.get_text(strip=True) if authors_elem else "Автор неизвестен",
                    "abstract": (p.get_text(strip=True) if p else "Аннотация отсутствует.")[:300],
                    "url": BASE + "/" + href,
                })
                if len(articles) >= 20:
                    break
            except Exception:
                continue
    return articles


if __name__ == "__main__":
    print("=== Journal ===")
    j = extract_journal_full()
    print(json.dumps(j, ensure_ascii=False, indent=2))
