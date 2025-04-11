# llm_function_call_demo.py

import openai
import json

import os

#from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# 模拟本地工具方法
def get_user_info(name):
    print("[Tool] get_user_info")
    return {"user_id": "123", "city": "上海"}

def get_user_orders(user_id):
    print("[Tool] get_user_orders")
    return {"orders": [100, 200, 300]}

def generate_discount(total_price):
    print("[Tool] generate_discount")
    if total_price > 500:
        return {"discount": "8折优惠"}
    return {"discount": "无优惠"}

TOOLS = {
    "get_user_info": get_user_info,
    "get_user_orders": get_user_orders,
    "generate_discount": generate_discount
}

# 定义 Function Call schema
functions_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_user_info",
            "description": "获取用户信息。返回json。user_id代表用户系统中的id。city是用户所在城市。",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_orders",
            "description": "获取用户订单。返回的数组，是用户最近几次用餐的消费金额。",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_discount",
            "description": "根据用户消费的总额，生成折扣。",
            "parameters": {
                "type": "object",
                "properties": {
                    "total_price": {"type": "number"}
                },
                "required": ["total_price"]
            }
        }
    }
]

# 聊天主逻辑
messages = [
    {"role": "system", "content": "你是一个智能助手。会执行tool call。当连续调用20次tool call，请在后面的一次消息中，不要继续返回tool calls。或提示用户告诉你所需要的信息。"},
    {"role": "system", "content": "如果要查询用户折扣，可以先通过用户名字查到他最近的三笔订单的金额。然后把这些订单总金额相加，就可以算出他的折扣。"},
    {"role": "user", "content": "帮我查一下张三的最近订单，计算一下他今年消费总金额，并且生成一个折扣推荐。"}
]

loop=0
while True:
    loop=loop+1
    print("\n#######################loop:",loop)
    print("Messages:",messages)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=functions_schema,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    # 检查是否还有 Tool Call
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        tool_call = msg.tool_calls[0]
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"检测到 Function Call: {name}, 参数: {args}")

        # 执行函数
        result = TOOLS[name](**args)

        # 从 schema 获取对应函数的 description
        description = next((f['function']['description'] for f in functions_schema if f['function']['name'] == name), "")
        content = f"{name}: {args} 结果是: {result}。"

        messages.append({
            "role": "function",
            "name": name,
            "content": content
        })

    else:
        # 没有函数调用，模型直接返回答案，结束循环
        print("\n模型最终回复:")
        print(msg.content)
        print("循环次数：",loop)
        break
