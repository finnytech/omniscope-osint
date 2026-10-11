"""
CYBER-SPECTRE-NEXUS: Global Geopolitical & Tactical OSINT News Engine
Real-time verified intelligence feeds from 200+ global news wires, crisis networks,
military dispatches, cyber emergency centers, and seismic monitors.
100% Free, Open, Zero API Key Required.
"""

import httpx
import logging
import asyncio
from typing import Dict, List, Optional
import time
import re
import xml.etree.ElementTree as ET

try:
    from backend.data.news_sources_200 import NEWS_SOURCES_200
except ImportError:
    from data.news_sources_200 import NEWS_SOURCES_200

logger = logging.getLogger("OSINTEngine")

NEWS_SOURCES = NEWS_SOURCES_200

class OSINTEngine:
    def __init__(self):
        self.sources = NEWS_SOURCES_200
        self.cached_news = []
        self.last_fetch = 0
        self.cache_ttl = 180  # 3 minutes cache for 200 feeds
        self.semaphore_limit = 5

    def list_sources(self) -> List[Dict]:
        return self.sources

    async def get_breaking_intelligence(
        self,
        category: str = "all",
        provider: str = "all",
        limit: int = 40
    ) -> Dict:
        """
        Retrieves real-time verified geopolitical, crisis, and tactical events from 200+ feeds.
        """
        now = time.time()
        if self.cached_news and (now - self.last_fetch < self.cache_ttl):
            filtered = self._filter_news(self.cached_news, category, provider)
            res_items = filtered[:limit]
            return {
                "total": len(filtered),
                "total_cached": len(self.cached_news),
                "events": res_items,
                "items": res_items,
                "providers_registered": len(self.sources) + 1,
                "source": "cache"
            }

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberSpectreNexus/3.0"}
        timeout = httpx.Timeout(4.0, connect=2.5)
        sem = asyncio.Semaphore(self.semaphore_limit)

        async with httpx.AsyncClient(timeout=timeout, headers=headers, follow_redirects=True) as client:
            async def fetch_feed(src: Dict) -> List[Dict]:
                feed_events = []
                async with sem:
                    try:
                        resp = await client.get(src["url"])
                        if resp.status_code == 200:
                            content = resp.text
                            # Handle XML parsing
                            try:
                                root = ET.fromstring(content)
                            except ET.ParseError:
                                # Clean potential non-xml prefix
                                cleaned = re.sub(r'^[^<]+', '', content).strip()
                                root = ET.fromstring(cleaned)

                            # RSS 2.0 items
                            items = root.findall('./channel/item')
                            if not items:
                                # RDF or Atom entries
                                items = root.findall('.//{http://purl.org/rss/1.0/}item') or \
                                        root.findall('.//{http://www.w3.org/2005/Atom}entry') or \
                                        root.findall('.//item') or \
                                        root.findall('.//entry')

                            for item in items[:8]:
                                title_elem = item.find('title')
                                link_elem = item.find('link')
                                date_elem = (
                                    item.find('pubDate') or
                                    item.find('published') or
                                    item.find('updated') or
                                    item.find('{http://purl.org/dc/elements/1.1/}date')
                                )
                                desc_elem = item.find('description') or item.find('summary')

                                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                                link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                                if not link and link_elem is not None and "href" in link_elem.attrib:
                                    link = link_elem.attrib["href"]

                                pub_date = date_elem.text.strip() if date_elem is not None and date_elem.text else time.strftime("%Y-%m-%dT%H:%M:%SZ")
                                desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""

                                if not title:
                                    continue

                                # Categorization & urgency detection
                                cat = src.get("category", "GEOPOLITICAL")
                                t_lower = title.lower()
                                if any(w in t_lower for w in ["breaking", "eilmeldung", "strike", "attack", "missile", "war", "explosion", "killed", "invade", "clashes", "nuclear"]):
                                    urgency = "HIGH"
                                    if cat == "GEOPOLITICAL":
                                        cat = "SECURITY"
                                elif any(w in t_lower for w in ["flood", "quake", "storm", "hurricane", "drought", "cyclone", "wildfire", "tsunami", "evacuate"]):
                                    urgency = "ALERT"
                                    cat = "CRISIS_DISASTER"
                                elif any(w in t_lower for w in ["malware", "ransomware", "zero-day", "cisa", "breach", "exploit", "cyberattack"]):
                                    urgency = "ALERT"
                                    cat = "CYBER_TECH"
                                else:
                                    urgency = "TACTICAL"

                                if "<" in desc and ">" in desc:
                                    desc = re.sub('<[^<]+?>', '', desc)

                                feed_events.append({
                                    "id": f"{src['id']}_{abs(hash(link or title))}",
                                    "provider_id": src["id"],
                                    "provider": src["name"],
                                    "category": cat,
                                    "title": title,
                                    "summary": desc[:220] + "..." if len(desc) > 220 else (desc or f"Verified report from {src['name']}."),
                                    "source": src["name"],
                                    "country": src.get("country", "Global"),
                                    "timestamp": pub_date,
                                    "url": link,
                                    "urgency": urgency
                                })
                    except Exception:
                        pass
                return feed_events

            async def fetch_emsc() -> List[Dict]:
                emsc_events = []
                async with sem:
                    try:
                        emsc_url = "https://www.seismicportal.eu/fdsnws/event/1/query?limit=15&format=json&minmag=3.5"
                        resp = await client.get(emsc_url)
                        if resp.status_code == 200:
                            data = resp.json()
                            for feat in data.get("features", []):
                                props = feat.get("properties", {})
                                mag = props.get("mag", 0.0)
                                flynn = props.get("flynn_region", "Seismic Zone")
                                emsc_events.append({
                                    "id": f"emsc_{feat.get('id')}",
                                    "provider_id": "emsc",
                                    "provider": "EMSC Euro-Med",
                                    "category": "CRISIS_DISASTER",
                                    "title": f"M {mag:.1f} Earthquake: {flynn}",
                                    "summary": f"Tectonic disturbance registered at {props.get('depth', 10)} km depth. Epicenter: {flynn}.",
                                    "source": "EMSC Seismological Portal",
                                    "country": flynn,
                                    "timestamp": props.get("time", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
                                    "url": f"https://www.emsc-csem.org/Earthquake/earthquake.php?id={feat.get('id')}",
                                    "urgency": "ALERT" if mag >= 5.0 else "MEDIUM"
                                })
                    except Exception:
                        pass
                return emsc_events

            # Concurrently gather all 200 feeds + EMSC
            tasks = [fetch_feed(src) for src in self.sources] + [fetch_emsc()]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            collected = []
            for res in results:
                if isinstance(res, list):
                    collected.extend(res)

        if collected:
            # Sort by urgency and then preserve order
            urgency_weights = {"HIGH": 3, "ALERT": 2, "TACTICAL": 1, "MEDIUM": 1}
            collected.sort(key=lambda x: urgency_weights.get(x.get("urgency", "TACTICAL"), 0), reverse=True)
            self.cached_news = collected
            self.last_fetch = now

        filtered = self._filter_news(self.cached_news, category, provider)
        res_items = filtered[:limit]
        return {
            "total": len(filtered),
            "total_cached": len(self.cached_news),
            "events": res_items,
            "items": res_items,
            "providers_registered": len(self.sources) + 1,
            "source": "live"
        }

    def _filter_news(self, events: List[Dict], category: str, provider: str) -> List[Dict]:
        res = events
        if category and category.lower() != "all":
            cat_lower = category.lower().replace("-", "_")
            res = [e for e in res if e.get("category", "").lower().replace("-", "_") == cat_lower]

        if provider and provider.lower() != "all":
            prov_lower = provider.lower()
            res = [
                e for e in res
                if e.get("provider_id", "").lower() == prov_lower
                or prov_lower in e.get("provider", "").lower()
            ]

        return res

osint_engine = OSINTEngine()
