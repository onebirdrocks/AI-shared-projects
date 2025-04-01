## Key Concepts\
async	声明一个异步函数
await	等待一个异步操作完成
asyncio	Python 内置的异步编程库
协程（Coroutine）	被 async def 定义的函数，是一种可以挂起并恢复执行的函数
事件循环（Event Loop）	控制协程何时执行的机制，是异步编程的核心


## Simple example

Example 1:
```
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

asyncio.run(say_hello())
```
Output
``` 
Hello
(等待1秒)
World
```


Example 2
```
import asyncio

async def say(msg, delay):
    print(f"Start: {msg}")
    await asyncio.sleep(delay)
    print(f"End: {msg}")

async def main():
    await asyncio.gather(
        say("Task 1", 2),
        say("Task 2", 1),
    )

asyncio.run(main())
```

这两个任务会并发执行，总耗时是最长的那一个（2秒），不是相加后的3秒。

## 和同步对比
同步写法
```
import time

def sync_task():
    time.sleep(1)
    print("Done")

sync_task()
```

异步写法
```
import asyncio

async def async_task():
    await asyncio.sleep(1)
    print("Done")

asyncio.run(async_task())
```


### 真实应用场景：并发请求接口
```
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"Fetched {url} with status {response.status}")
            return await response.text()

async def main():
    urls = ["https://example.com", "https://httpbin.org/get"]
    tasks = [fetch(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())
```