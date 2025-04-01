import aiohttp
import asyncio
import logging
import random

# 配置 logging
logger = logging.getLogger("fetcher")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# 全局 session（复用连接）
session = None

# 异步抓取 HTML 内容，带重试机制
async def fetch_html(url, timeout=10, max_retries=3):
    global session
    if session is None:
        session = aiohttp.ClientSession()

    attempt = 0
    while attempt < max_retries:
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    logger.info(f"✅ Success: {url}")
                    return await response.text()
                else:
                    logger.warning(f"⚠️ Non-200 status {response.status} for {url}")
                    return ""
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            attempt += 1
            wait_time = 2 ** attempt + random.random()
            logger.warning(f"🔁 Retry {attempt}/{max_retries} for {url} after {wait_time:.1f}s due to: {e}")
            await asyncio.sleep(wait_time)
        except Exception as e:
            logger.error(f"❌ Unexpected error for {url}: {e}")
            return ""

    logger.error(f"🚫 Failed after {max_retries} retries: {url}")
    return ""

# 优雅关闭 session
async def close_session():
    global session
    if session:
        await session.close()
        session = None
