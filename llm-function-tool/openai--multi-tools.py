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
            "description": "获取用户信息",
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
            "description": "获取用户订单",
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
            "description": "生成折扣",
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
   {"role": "system", "content": "你是一个智能助手，会执行和tool calls，当你发现tool call循环次数超过10次，就不要继续调用了。"},
    {"role": "user", "content": "帮我查一下张三的最近订单，计算一下他今年消费总金额，并且生成一个折扣推荐。"}
]

loop =0

while True:
    loop = loop + 1
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=functions_schema,
        tool_choice="auto"
    )

    msg = response.choices[0].message
    print("\n\n\n################")
    print("loop:",loop)
    print("message history:",messages)
    print("response:", msg)

    # 检查是否还有 Tool Call
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print("tool calls length:",len(msg.tool_calls))
        tool_call = msg.tool_calls[0]
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"检测到 Function Call: {name}, 参数: {args}")

        # 执行函数
        result = TOOLS[name](**args)
        print("result:",result)

        # 添加函数执行结果到消息历史
        messages.append({
            "role": "function",
            "name": name,
            "content": json.dumps(result)
        })
        
    else:
        # 没有函数调用，模型直接返回答案，结束循环
        print("\n模型最终回复:")
        print(msg.content)
        break
