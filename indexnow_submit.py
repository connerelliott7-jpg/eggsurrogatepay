#!/usr/bin/env python3
"""
IndexNow submission for eggsurrogatepay.com
Run after every deploy: python3 indexnow_submit.py
Submits all sitemap URLs to IndexNow, which notifies Google and Bing.
"""

import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

HOST = "eggsurrogatepay.com"
KEY = "ac6dfc1a10900220f167bf7a53cdf49e"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

def get_urls_from_sitemap():
    print(f"Fetching sitemap: {SITEMAP_URL}")
    with urllib.request.urlopen(SITEMAP_URL, timeout=10) as resp:
        content = resp.read()
    root = ET.fromstring(content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]
    print(f"Found {len(urls)} URLs in sitemap")
    return urls

def submit_to_indexnow(urls):
    # IndexNow API accepts up to 10,000 URLs per request
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            print(f"IndexNow response: {status}")
            if status == 200:
                print(f"Success — {len(urls)} URLs submitted to IndexNow")
            elif status == 202:
                print(f"Accepted — {len(urls)} URLs queued for crawling")
            else:
                print(f"Unexpected status: {status}")
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
        body = e.read().decode("utf-8", errors="replace")
        if body:
            print(f"Response body: {body}")
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}")

if __name__ == "__main__":
    urls = get_urls_from_sitemap()
    if urls:
        submit_to_indexnow(urls)
    else:
        print("No URLs found — check sitemap")
