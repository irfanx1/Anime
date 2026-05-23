#@cantarellabots
from cantarella.core.proxy import get_random_proxy, get_proxy_dict
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://aniwatchtv.to"
ANILIST_URL = "https://graphql.anilist.co"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# ── AniList GraphQL search — always reliable ─────────────────────────────────
ANILIST_QUERY = """
query ($search: String) {
  Page(perPage: 10) {
    media(search: $search, type: ANIME, sort: SEARCH_MATCH) {
      id
      title { english romaji native }
      status
      episodes
      type
      format
      coverImage { large medium }
      genres
      averageScore
      startDate { year }
    }
  }
}
"""

def search_anime_anilist(query: str) -> list:
    """Search anime using AniList GraphQL API — most reliable source."""
    try:
        resp = requests.post(
            ANILIST_URL,
            json={"query": ANILIST_QUERY, "variables": {"search": query}},
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        if resp.status_code != 200:
            return []

        data = resp.json()
        media_list = data.get("data", {}).get("Page", {}).get("media", [])

        results = []
        for item in media_list:
            title_data = item.get("title", {})
            title = (
                title_data.get("english") or
                title_data.get("romaji") or
                title_data.get("native") or
                "Unknown"
            )
            anime_format = item.get("format") or item.get("type") or "ANIME"
            year = (item.get("startDate") or {}).get("year") or ""
            label = f"{anime_format}" + (f" • {year}" if year else "")

            results.append({
                "title": title,
                "id": f"anilist_{item.get('id')}",
                "type": label,
                "url": f"https://anilist.co/anime/{item.get('id')}",
                "anilist_id": item.get("id"),
                "cover": (item.get("coverImage") or {}).get("large") or "",
                "episodes": item.get("episodes") or "?",
                "status": item.get("status") or "",
                "score": item.get("averageScore") or "",
            })

        return results

    except Exception as e:
        print(f"[AniList search error] {e}")
        return []


def search_anime_animetsu(query: str) -> list:
    """Search via animetsu scraper (fallback)."""
    try:
        from cantarella.scraper.animetsu import AnimetsuScraper
        return AnimetsuScraper().search_anime(query)
    except Exception as e:
        print(f"[Animetsu search error] {e}")
        return []


def search_anime_aniwatch(query: str) -> list:
    """Search via aniwatchtv.to (fallback)."""
    try:
        from curl_cffi import requests as c_requests
        search_url = f"{BASE_URL}/search?keyword={query.replace(' ', '+')}"
        session = c_requests.Session()
        proxy_dict = get_proxy_dict(get_random_proxy())
        if proxy_dict:
            session.proxies.update(proxy_dict)
        resp = session.get(search_url, headers=HEADERS, impersonate="chrome", timeout=15)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for item in soup.select(".film_list-wrap .flw-item"):
            title_elem = item.select_one(".film-name a")
            if not title_elem:
                continue
            title = title_elem.get("title") or title_elem.text.strip()
            href = title_elem.get("href", "")
            anime_id = href.split("/")[-1].split("?")[0]
            type_elem = item.select_one(".fdi-item")
            anime_type = type_elem.text.strip() if type_elem else "Unknown"
            results.append({
                "title": title,
                "id": anime_id,
                "type": anime_type,
                "url": f"{BASE_URL}{href}" if href.startswith("/") else f"{BASE_URL}/{href}",
            })
            if len(results) >= 10:
                break
        return results
    except Exception as e:
        print(f"[Aniwatch search error] {e}")
        return []


def search_anime(query: str, source: str = "anilist") -> list:
    """
    Search anime with automatic fallback chain:
    1. AniList GraphQL (most reliable, always available)
    2. Animetsu scraper
    3. Aniwatchtv scraper
    """
    # Always try AniList first — it never blocks and has the most data
    results = search_anime_anilist(query)
    if results:
        return results

    # Fallback to animetsu
    if source == "animetsu":
        results = search_anime_animetsu(query)
        if results:
            return results

    # Final fallback to aniwatch scraper
    results = search_anime_aniwatch(query)
    return results


if __name__ == "__main__":
    print(search_anime("naruto"))
