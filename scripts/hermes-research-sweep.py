#!/usr/bin/env python3
"""
hermes-research-sweep.py

Multi-source, multilingual academic research sweep across the 7 canonical
AI-agent improvement categories identified from citation analysis (Aug 2026):

  1. Reasoning + Planning
  2. Tool Use / Function Calling
  3. Memory Architecture
  4. Multi-Agent Systems / Collaboration
  5. Agent Evaluation / Benchmarking
  6. Agent Evolution / Self-Improvement
  7. Agentic RAG / Context Management

Sources (multilingual):
  - arXiv (cs.AI, cs.CL, cs.MA, cs.LG) — via web search + HTML search UI
  - Semantic Scholar (S2) API — citation-ranked recent papers
  - Papers With Code — trending leaderboards
  - Hugging Face Papers — community-voted recent releases
  - OpenAlex — open scholarly metadata
  - HAL (French/EU source)
  - CNKI proxy via arXiv (Chinese institution author search)
  - AMiner (Chinese AI/CS graph)
  - J-STAGE (Japanese)
  - CyberLeninka (Russian/Eastern European OA)

Output:
  ~/.hermes/cache/research/hermes-research-latest.json
  ~/.hermes/cache/research/hermes-research-YYYY-MM-DD.json
  Prints a plain-text digest to stdout if new papers found (cron delivery).
  Prints nothing if no new papers above threshold (silent cron tick).

Cache:
  ~/.hermes/cache/research/seen_papers.json  (rolling SHA256 of arXiv IDs)

Usage:
  python3 ~/.hermes/scripts/hermes-research-sweep.py [--dry-run] [--force]
  # As a cron script (no_agent=True for data collection phase)
"""

import json
import os
import sys
import hashlib
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

# ── Paths ─────────────────────────────────────────────────────────────────
CACHE_DIR = Path.home() / ".hermes" / "cache" / "research"
SEEN_FILE = CACHE_DIR / "seen_papers.json"
OUTPUT_LATEST = CACHE_DIR / "hermes-research-latest.json"
OUTPUT_DATED = CACHE_DIR / f"hermes-research-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json"
MAX_SEEN = 2000   # rolling window

DRY_RUN = "--dry-run" in sys.argv
FORCE = "--force" in sys.argv

# ── Research categories and search terms ──────────────────────────────────
CATEGORIES = {
    "reasoning_planning": {
        "label": "Reasoning + Planning",
        "queries": [
            "LLM agent reasoning planning chain of thought 2026",
            "language model planning task decomposition 2026",
            "tree of thoughts Monte Carlo LLM 2025 2026",
            "process reward model step verification LLM agent",
            "test-time compute scaling reasoning agent 2026",
        ],
        "arxiv_cats": ["cs.AI", "cs.CL", "cs.LG"],
    },
    "tool_use": {
        "label": "Tool Use / Function Calling",
        "queries": [
            "LLM tool use function calling agent 2026",
            "language model API tool learning 2026",
            "model context protocol MCP agent tool 2026",
            "tool creation agent CREATOR self-generated 2026",
            "multi-tool composition error recovery agent 2026",
        ],
        "arxiv_cats": ["cs.AI", "cs.CL"],
    },
    "memory": {
        "label": "Memory Architecture",
        "queries": [
            "LLM agent memory architecture episodic semantic 2026",
            "agent memory consolidation retrieval augmented 2026",
            "MemGPT long-term memory agent 2025 2026",
            "agent memory compression eviction strategy 2026",
            "self-evolving memory knowledge graph agent 2026",
        ],
        "arxiv_cats": ["cs.AI", "cs.CL", "cs.IR"],
    },
    "multi_agent": {
        "label": "Multi-Agent Systems / Collaboration",
        "queries": [
            "multi-agent LLM collaboration 2026",
            "multi-agent debate consensus reasoning 2026",
            "LLM agent orchestration workflow 2026",
            "agent communication protocol emergence 2026",
            "multiagent finetuning self-improvement 2026",
        ],
        "arxiv_cats": ["cs.MA", "cs.AI", "cs.CL"],
    },
    "evaluation": {
        "label": "Agent Evaluation / Benchmarking",
        "queries": [
            "LLM agent benchmark evaluation 2026",
            "agent trajectory evaluation process reward 2026",
            "LLM judge evaluation metric agent 2026",
            "SWE-bench WebArena OSWorld agent evaluation 2026",
            "agent evaluation alignment safety benchmark 2026",
        ],
        "arxiv_cats": ["cs.AI", "cs.CL", "cs.SE"],
    },
    "self_improvement": {
        "label": "Agent Evolution / Self-Improvement",
        "queries": [
            "LLM agent self-improvement fine-tuning 2026",
            "agent skill learning from experience trajectory 2026",
            "autonomous agent evolution curriculum 2026",
            "reinforcement learning LLM agent policy improvement 2026",
            "agent self-reflection verbal reinforcement 2025 2026",
        ],
        "arxiv_cats": ["cs.AI", "cs.LG", "cs.CL"],
    },
    "agentic_rag": {
        "label": "Agentic RAG / Context Management",
        "queries": [
            "agentic RAG retrieval augmented generation agent 2026",
            "long context management compression agent 2026",
            "knowledge graph retrieval agent 2026",
            "adaptive retrieval agent orchestration 2026",
            "context window management agent memory 2026",
        ],
        "arxiv_cats": ["cs.IR", "cs.AI", "cs.CL"],
    },
}

# Multilingual supplementary sources
MULTILINGUAL_SOURCES = {
    "zh": {
        "label": "Chinese (via AMiner / arXiv Chinese institutions)",
        "aminer_queries": [
            "agent memory architecture",
            "multi-agent LLM collaboration",
            "LLM reasoning planning",
            "agent self-improvement trajectory",
            "agentic RAG retrieval",
            "agent evaluation benchmark",
            "LLM tool use function calling",
        ],
    },
    "ja": {
        "label": "Japanese (J-STAGE)",
        "jstage_queries": [
            "LLM agent",
            "language model planning",
            "multi-agent system",
            "agent memory retrieval",
        ],
    },
    "fr": {
        "label": "French (HAL)",
        "hal_queries": [
            "agent LLM raisonnement planification",
            "agent mémoire architecture",
            "système multi-agent LLM",
            "agent amélioration automatique",
            "évaluation agent langage",
        ],
    },
    "ru": {
        "label": "Russian (CyberLeninka)",
        "cyberleninka_queries": [
            "языковая модель агент рассуждение",
            "мультиагентная система LLM",
            "LLM agent memory",
            "agent self-improvement reinforcement",
        ],
    },
    "ko": {
        "label": "Korean (via arXiv Korean institutions)",
        "arxiv_queries": [
            "agent LLM KAIST Seoul National University 2026",
            "language model reasoning POSTECH Korea 2026",
            "multi-agent system Korean university 2025 2026",
        ],
    },
}

# HuggingFace Papers trending URL
HF_PAPERS_URL = "https://huggingface.co/papers"
# Papers With Code trending
PWC_TRENDING = "https://paperswithcode.com/latest"

# ── Helpers ───────────────────────────────────────────────────────────────

def paper_key(arxiv_id: str) -> str:
    return hashlib.sha256(arxiv_id.encode()).hexdigest()[:16]


def load_seen() -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if SEEN_FILE.exists():
        try:
            return json.loads(SEEN_FILE.read_text())
        except Exception:
            return {"seen": [], "last_updated": None, "last_sweep": None}
    return {"seen": [], "last_updated": None, "last_sweep": None}


def save_seen(seen: dict) -> None:
    if len(seen["seen"]) > MAX_SEEN:
        seen["seen"] = seen["seen"][-MAX_SEEN:]
    seen["last_updated"] = datetime.now(timezone.utc).isoformat()
    SEEN_FILE.write_text(json.dumps(seen, indent=2))


def fetch(url: str, timeout: int = 15) -> str:
    """Fetch URL, return text or empty string on error."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "HermesResearch/1.0 (research-sweep; mailto:research@hermes.local)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def arxiv_id_valid(arxiv_id: str) -> bool:
    """Filter out fake DOI-derived IDs like 9027.37650."""
    try:
        parts = arxiv_id.split(".")
        return int(parts[0]) < 10000
    except Exception:
        return False


# ── arXiv listing sweep (most reliable for recency) ───────────────────────

def sweep_arxiv_listings(categories: list[str]) -> list[dict]:
    """Walk arXiv category listing pages for very recent papers."""
    papers = []
    for cat in set(categories):
        url = f"https://arxiv.org/list/{cat}/recent"
        html = fetch(url, timeout=20)
        if not html:
            continue
        # Extract arXiv IDs from listing
        ids_found = re.findall(r'arXiv:(\d{4}\.\d{4,5})', html)
        titles = re.findall(r'class="title[^"]*"[^>]*>\s*<span[^>]*>Title:</span>\s*(.*?)</span>', html)
        # Simple parse: collect IDs + try to pair with nearby titles
        for i, arxiv_id in enumerate(ids_found):
            if not arxiv_id_valid(arxiv_id):
                continue
            title = titles[i] if i < len(titles) else ""
            title = re.sub(r'<[^>]+>', '', title).strip()
            papers.append({
                "id": arxiv_id,
                "title": title or f"[arXiv:{arxiv_id}]",
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "source": f"arxiv-listing:{cat}",
                "category": None,  # assigned by caller
            })
        time.sleep(0.5)
    return papers


# ── arXiv HTML search (keyword-matched, date-sorted) ──────────────────────

def search_arxiv_html(query: str, max_results: int = 10) -> list[dict]:
    """Use arXiv HTML search interface (not API — API hangs on this host)."""
    q = urllib.parse.quote(query)
    url = f"https://arxiv.org/search/?searchtype=all&query={q}&start=0&order=-submitted_date"
    html = fetch(url, timeout=20)
    if not html:
        return []
    ids = re.findall(r'arXiv:(\d{4}\.\d{4,5})', html)
    titles = re.findall(r'class="title[^"]*"[^>]*>\s*(.*?)\s*</p>', html, re.DOTALL)
    results = []
    for i, arxiv_id in enumerate(ids[:max_results]):
        if not arxiv_id_valid(arxiv_id):
            continue
        title = titles[i] if i < len(titles) else ""
        title = re.sub(r'<[^>]+>', '', title).strip()
        results.append({
            "id": arxiv_id,
            "title": title or f"[arXiv:{arxiv_id}]",
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "source": "arxiv-search",
            "category": None,
        })
    return results


# ── Semantic Scholar API ───────────────────────────────────────────────────

def search_semantic_scholar(query: str, max_results: int = 5) -> list[dict]:
    """Query S2 search API. Unauthenticated: 1 req/sec limit."""
    q = urllib.parse.quote(query)
    url = (f"https://api.semanticscholar.org/graph/v1/paper/search"
           f"?query={q}&limit={max_results}"
           f"&fields=title,externalIds,year,citationCount,influentialCitationCount")
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        data = json.loads(text)
        papers = []
        for p in data.get("data", []):
            arxiv_id = p.get("externalIds", {}).get("ArXiv", "")
            if not arxiv_id or not arxiv_id_valid(arxiv_id):
                continue
            papers.append({
                "id": arxiv_id,
                "title": p.get("title", ""),
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "source": "semantic-scholar",
                "citations": p.get("citationCount", 0),
                "year": p.get("year"),
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── HAL (French/EU) ───────────────────────────────────────────────────────

def search_hal(query: str, max_results: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    url = (f"https://api.archives-ouvertes.fr/search/"
           f"?q={q}&rows={max_results}&fl=title_s,authFullName_s,uri_s,doiId_s,producedDate_s&wt=json&sort=producedDate_s+desc")
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        data = json.loads(text)
        papers = []
        for doc in data.get("response", {}).get("docs", []):
            title = doc.get("title_s", [""])[0] if isinstance(doc.get("title_s"), list) else doc.get("title_s", "")
            uri = doc.get("uri_s", "")
            papers.append({
                "id": uri,
                "title": title,
                "url": uri,
                "source": "hal",
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── AMiner (Chinese AI/CS) ────────────────────────────────────────────────

def search_aminer(query: str, max_results: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    url = f"https://api.aminer.org/api/search/pub?query={q}&size={max_results}"
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        data = json.loads(text)
        papers = []
        for p in data.get("result", [])[:max_results]:
            title = p.get("title", "")
            urls = p.get("urls", [])
            link = urls[0] if urls else ""
            # Try to extract arXiv ID
            arxiv_id = ""
            for u in urls:
                m = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', u)
                if m and arxiv_id_valid(m.group(1)):
                    arxiv_id = m.group(1)
                    break
            papers.append({
                "id": arxiv_id or link,
                "title": title,
                "url": link or f"https://www.aminer.org/search?q={q}",
                "source": "aminer",
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── OpenAlex ──────────────────────────────────────────────────────────────

def search_openalex(query: str, max_results: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    # Filter for recent (2025+) papers to avoid old results
    url = (f"https://api.openalex.org/works?search={q}&per-page={max_results}"
           f"&filter=publication_year:2025|2026&sort=cited_by_count:desc"
           f"&mailto=research@hermes.local")
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        data = json.loads(text)
        papers = []
        for w in data.get("results", []):
            title = w.get("title", "")
            doi = w.get("doi", "")
            # Try to get arXiv ID from locations
            arxiv_id = ""
            for loc in w.get("locations", []):
                lurl = loc.get("landing_page_url", "") or loc.get("pdf_url", "") or ""
                m = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', lurl)
                if m and arxiv_id_valid(m.group(1)):
                    arxiv_id = m.group(1)
                    break
            link = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else doi or ""
            papers.append({
                "id": arxiv_id or doi or title[:40],
                "title": title,
                "url": link,
                "source": "openalex",
                "citations": w.get("cited_by_count", 0),
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── Crossref (DOI-based, high quality) ───────────────────────────────────

def search_crossref(query: str, max_results: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    url = (f"https://api.crossref.org/works?query={q}&rows={max_results}"
           f"&filter=from-pub-date:2025&sort=is-referenced-by-count&order=desc"
           f"&mailto=research@hermes.local")
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        data = json.loads(text)
        papers = []
        for item in data.get("message", {}).get("items", []):
            titles = item.get("title", [""])
            title = titles[0] if titles else ""
            doi = item.get("DOI", "")
            url_out = item.get("URL", "") or f"https://doi.org/{doi}"
            papers.append({
                "id": doi or title[:40],
                "title": title,
                "url": url_out,
                "source": "crossref",
                "citations": item.get("is-referenced-by-count", 0),
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── J-STAGE (Japanese) ────────────────────────────────────────────────────

def search_jstage(query: str, max_results: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    url = f"https://api.jstage.jst.go.jp/articles/_search?text={q}&count={max_results}&lang=en"
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        root = ET.fromstring(text)
        papers = []
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title_el = entry.find("atom:title", ns)
            link_el = entry.find("atom:link", ns)
            title = title_el.text if title_el is not None else ""
            link = link_el.get("href", "") if link_el is not None else ""
            papers.append({
                "id": link or title[:40],
                "title": title,
                "url": link,
                "source": "jstage",
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── CyberLeninka (Russian/Eastern European OA) ───────────────────────────

def search_cyberleninka(query: str, max_results: int = 5) -> list[dict]:
    q = urllib.parse.quote(query)
    url = f"https://cyberleninka.ru/api/1/search?q={q}&size={max_results}"
    text = fetch(url, timeout=15)
    if not text:
        return []
    try:
        data = json.loads(text)
        papers = []
        for item in data.get("response", {}).get("docs", [])[:max_results]:
            title = item.get("article_name", "")
            link = item.get("url", "")
            papers.append({
                "id": link or title[:40],
                "title": title,
                "url": f"https://cyberleninka.ru{link}" if link.startswith("/") else link,
                "source": "cyberleninka",
                "category": None,
            })
        return papers
    except Exception:
        return []


# ── HuggingFace Papers (community-voted trending) ─────────────────────────

def scrape_hf_papers(max_results: int = 15) -> list[dict]:
    """Scrape HuggingFace daily papers page for arXiv IDs."""
    html = fetch(HF_PAPERS_URL, timeout=20)
    if not html:
        return []
    ids = re.findall(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', html)
    papers = []
    for arxiv_id in ids[:max_results]:
        if arxiv_id_valid(arxiv_id):
            papers.append({
                "id": arxiv_id,
                "title": f"[arXiv:{arxiv_id}]",
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "source": "huggingface-papers",
                "category": "trending",
            })
    return papers


# ── Papers With Code (trending leaderboards) ──────────────────────────────

def scrape_pwc(max_results: int = 15) -> list[dict]:
    """Scrape Papers With Code latest page for arXiv IDs."""
    html = fetch(PWC_TRENDING, timeout=20)
    if not html:
        return []
    ids = re.findall(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', html)
    papers = []
    seen_ids: set[str] = set()
    for arxiv_id in ids:
        if arxiv_id_valid(arxiv_id) and arxiv_id not in seen_ids:
            seen_ids.add(arxiv_id)
            papers.append({
                "id": arxiv_id,
                "title": f"[arXiv:{arxiv_id}]",
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "source": "papers-with-code",
                "category": "trending",
            })
        if len(papers) >= max_results:
            break
    return papers


# ── Main sweep ────────────────────────────────────────────────────────────

def run_sweep() -> tuple[list[dict], list[dict]]:
    """
    Returns (all_papers, new_papers).
    all_papers: every paper found this run
    new_papers: papers not in the seen cache
    """
    seen = load_seen()
    seen_keys = set(seen["seen"])
    all_papers: list[dict] = []

    print(f"[hermes-research-sweep] Starting sweep at {datetime.now(timezone.utc).isoformat()}", file=sys.stderr)
    print(f"[hermes-research-sweep] Known papers: {len(seen_keys)}", file=sys.stderr)

    fetched_arxiv_cats: set[str] = set()  # track already-fetched listing pages

    for cat_key, cat in CATEGORIES.items():
        print(f"[hermes-research-sweep] Category: {cat['label']}", file=sys.stderr)

        # 1. arXiv listing walk (most recent, pre-search-engine)
        # Deduplicate cats before listing — cs.AI appears across multiple categories
        # and sweep_arxiv_listings already deduplicates internally per run but we skip
        # re-fetching listings already done by a prior category in THIS sweep
        arxiv_cats: list[str] = [c for c in (cat.get("arxiv_cats") or []) if c not in fetched_arxiv_cats]
        fetched_arxiv_cats.update(arxiv_cats)
        listing_papers = sweep_arxiv_listings(arxiv_cats)
        for p in listing_papers:
            p["category"] = cat_key
        all_papers.extend(listing_papers)
        time.sleep(1)

        # 2. arXiv HTML search per query — all 5 queries, not just 3
        for query in cat["queries"]:
            papers = search_arxiv_html(query, max_results=8)
            for p in papers:
                p["category"] = cat_key
            all_papers.extend(papers)
            time.sleep(1.2)

        # 3. Semantic Scholar (top citations) — all 5 queries, not just 2
        for query in cat["queries"]:
            papers = search_semantic_scholar(query, max_results=5)
            for p in papers:
                p["category"] = cat_key
            all_papers.extend(papers)
            time.sleep(1.5)  # S2 rate limit

        # 4. OpenAlex (citation-ranked, recent) — top 2 queries
        for query in cat["queries"][:2]:
            papers = search_openalex(query, max_results=5)
            for p in papers:
                p["category"] = cat_key
            all_papers.extend(papers)
            time.sleep(1)

        # 5. Crossref (DOI-backed, high quality) — top query per category
        papers = search_crossref(cat["queries"][0], max_results=5)
        for p in papers:
            p["category"] = cat_key
        all_papers.extend(papers)
        time.sleep(1)

    # 5. Multilingual sources
    print("[hermes-research-sweep] Multilingual sweep...", file=sys.stderr)

    # HAL (French)
    for q in MULTILINGUAL_SOURCES["fr"]["hal_queries"]:
        papers = search_hal(q, max_results=3)
        for p in papers:
            p["category"] = "multilingual_fr"
        all_papers.extend(papers)
        time.sleep(0.8)

    # AMiner (Chinese)
    for q in MULTILINGUAL_SOURCES["zh"]["aminer_queries"]:
        papers = search_aminer(q, max_results=3)
        for p in papers:
            p["category"] = "multilingual_zh"
        all_papers.extend(papers)
        time.sleep(1)

    # J-STAGE (Japanese)
    for q in MULTILINGUAL_SOURCES["ja"]["jstage_queries"]:
        papers = search_jstage(q, max_results=3)
        for p in papers:
            p["category"] = "multilingual_ja"
        all_papers.extend(papers)
        time.sleep(0.8)

    # CyberLeninka (Russian)
    for q in MULTILINGUAL_SOURCES["ru"]["cyberleninka_queries"]:
        papers = search_cyberleninka(q, max_results=3)
        for p in papers:
            p["category"] = "multilingual_ru"
        all_papers.extend(papers)
        time.sleep(0.8)

    # Korean (via arXiv institution search — no native API)
    print("[hermes-research-sweep] Korean (arXiv institution search)...", file=sys.stderr)
    for q in MULTILINGUAL_SOURCES["ko"]["arxiv_queries"]:
        papers = search_arxiv_html(q, max_results=5)
        for p in papers:
            p["category"] = "multilingual_ko"
        all_papers.extend(papers)
        time.sleep(1)

    # HuggingFace Papers (trending — broad signal, post-filter by apply job)
    print("[hermes-research-sweep] HuggingFace Papers trending...", file=sys.stderr)
    hf_papers = scrape_hf_papers(max_results=20)
    all_papers.extend(hf_papers)
    time.sleep(1)

    # Papers With Code (leaderboard trending)
    print("[hermes-research-sweep] Papers With Code trending...", file=sys.stderr)
    pwc_papers = scrape_pwc(max_results=20)
    all_papers.extend(pwc_papers)
    time.sleep(1)

    # Deduplicate by ID
    seen_this_run: set[str] = set()
    unique_papers: list[dict] = []
    for p in all_papers:
        pid = p["id"]
        if pid and pid not in seen_this_run:
            seen_this_run.add(pid)
            unique_papers.append(p)

    # Filter to new papers only
    new_papers = [p for p in unique_papers if paper_key(p["id"]) not in seen_keys]

    print(f"[hermes-research-sweep] Total unique: {len(unique_papers)}, new: {len(new_papers)}", file=sys.stderr)

    # Update seen cache
    if not DRY_RUN:
        for p in new_papers:
            key = paper_key(p["id"])
            if key not in seen_keys:
                seen["seen"].append(key)
        seen["last_sweep"] = datetime.now(timezone.utc).isoformat()
        save_seen(seen)

    return unique_papers, new_papers


def build_output(new_papers: list[dict], all_papers: list[dict]) -> dict:
    """Build structured JSON output for the cron system and apply job."""
    by_category: dict[str, list[dict]] = {}
    for p in new_papers:
        cat = p.get("category", "unknown")
        by_category.setdefault(cat, []).append(p)

    return {
        "sweep_date": datetime.now(timezone.utc).isoformat(),
        "new_paper_count": len(new_papers),
        "total_scanned": len(all_papers),
        "categories": {k: v["label"] for k, v in CATEGORIES.items()},
        "new_papers_by_category": by_category,
        "new_papers_flat": new_papers,
    }


def format_digest(output: dict) -> str:
    """Plain-text digest for cron delivery."""
    lines = [
        f"=== Hermes Research Sweep — {output['sweep_date'][:10]} ===",
        f"{output['new_paper_count']} new papers across {output['total_scanned']} scanned",
        "",
    ]
    for cat_key, papers in output["new_papers_by_category"].items():
        cat_label = CATEGORIES.get(cat_key, {}).get("label", cat_key)
        lines.append(f"[{cat_label}] ({len(papers)} new)")
        for p in papers[:5]:  # top 5 per category in digest
            cites = f" [{p.get('citations', 0)} cites]" if p.get("citations") else ""
            lines.append(f"  - {p['title'][:80]}{cites}")
            lines.append(f"    {p['url']}")
        if len(papers) > 5:
            lines.append(f"  ... and {len(papers)-5} more (see JSON output)")
        lines.append("")
    lines.append(f"Full output: {OUTPUT_LATEST}")
    return "\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────

def main():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    all_papers, new_papers = run_sweep()
    output = build_output(new_papers, all_papers)

    if not DRY_RUN:
        OUTPUT_LATEST.write_text(json.dumps(output, indent=2))
        OUTPUT_DATED.write_text(json.dumps(output, indent=2))
        print(f"[hermes-research-sweep] Wrote {OUTPUT_LATEST}", file=sys.stderr)

    # Stdout: deliver digest only if new papers found (silent cron tick if empty)
    if new_papers or FORCE:
        print(format_digest(output))
    else:
        print(f"[hermes-research-sweep] No new papers found — silent tick", file=sys.stderr)


if __name__ == "__main__":
    main()
