from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag

def extract_links(html, base_url=None, include_images=False, same_domain_only=False):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    base_domain = urlparse(base_url).netloc if base_url else None

    def add_url(raw_url):
        # 去掉 #锚点
        clean_url, _ = urldefrag(raw_url)
        full_url = urljoin(base_url, clean_url)

        # 限定同域
        if same_domain_only:
            if urlparse(full_url).netloc != base_domain:
                return

        links.add(full_url)

    # 提取 <a href="">
    for tag in soup.find_all('a', href=True):
        add_url(tag['href'])

    # 可选提取 <img src="">
    if include_images:
        for tag in soup.find_all('img', src=True):
            add_url(tag['src'])

        # 同时支持 <script src=""> 和 <link href="">
        for tag in soup.find_all('script', src=True):
            add_url(tag['src'])

        for tag in soup.find_all('link', href=True):
            add_url(tag['href'])

    return list(links)
