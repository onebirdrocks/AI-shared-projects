# 🕸️ Async Crawler & Downloader

一个基于 Python 异步编程的轻量级爬虫 + 下载器项目，支持并发抓取网页资源、提取链接并异步保存文件。

## ✨ 项目功能

- 异步请求网页内容（基于 `aiohttp`）
- 使用 `BeautifulSoup` 提取页面中的链接、图片、脚本等资源
- 自动识别文件类型保存，避免重名
- 日志记录 + 自动重试机制
- 可通过命令行传入起始 URL
- 支持同域名筛选、图片资源控制

## 📦 安装依赖

```bash
pip install -r requirements.txt

## 运行
python main.py https://example.com