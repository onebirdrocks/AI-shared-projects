import sys
import asyncio
from fetcher import fetch_html, close_session
from parser import extract_links
from downloader import download_all

async def main():
    if len(sys.argv) < 2:
        print("用法: python main.py https://example.com")
        return

    start_url = sys.argv[1]
    html = await fetch_html(start_url)
    links = extract_links(html, base_url=start_url, include_images=True, same_domain_only=True)
    await download_all(links)
    await close_session()

if __name__ == "__main__":
    asyncio.run(main())
