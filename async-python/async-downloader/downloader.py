import aiohttp
import asyncio
import os
import logging
import hashlib
import mimetypes
from urllib.parse import urlparse

# 配置日志
logger = logging.getLogger("downloader")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# 确保 downloads 目录存在
os.makedirs("downloads", exist_ok=True)

visited_file = "visited_urls.txt"

def is_visited(url):
    if not os.path.exists(visited_file):
        return False
    with open(visited_file, "r") as f:
        return url in f.read()

def mark_visited(url):
    with open(visited_file, "a") as f:
        f.write(url + "\n")

# 主入口，下载所有资源
async def download_all(links):
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in links]
        await asyncio.gather(*tasks)

# 下载单个文件
async def download_file(session, url):
    try:
        if is_visited(url):
            logger.info(f"⏩ Skipped (already downloaded): {url}")
            return
        
        async with session.get(url, timeout=15) as response:
            if response.status != 200:
                logger.warning(f"⚠️ Failed ({response.status}) {url}")
                return

            content = await response.read()

            # 自动获取文件扩展名
            content_type = response.headers.get("Content-Type", "")
            ext = mimetypes.guess_extension(content_type.split(";")[0]) or ".bin"

            # 构建安全的文件名
            parsed = urlparse(url)
            basename = os.path.basename(parsed.path) or "index"
            hash_part = hashlib.md5(url.encode()).hexdigest()[:6]
            filename = f"{basename}_{hash_part}{ext}"

            filepath = os.path.join("downloads", filename)
            with open(filepath, "wb") as f:
                f.write(content)

            logger.info(f"✅ Downloaded: {url} -> {filename}")
            mark_visited(url)
            
    except Exception as e:
        logger.error(f"❌ Error downloading {url}: {e}")
