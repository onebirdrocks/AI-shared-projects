
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 读取 .env 中的 OPENAI_API_KEY
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ 定义两个 tool（注意是 tools，不是 functions）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取某城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如 北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取某城市的当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如 北京、纽约"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# ✅ 用户输入
messages = [
    {"role": "user", "content": "现在北京的天气和时间怎么样？"}
]

# ✅ 使用 GPT-4 Turbo 正确模型名：gpt-4-1106-preview
response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

tool_calls = response.choices[0].message.tool_calls
messages.append(response.choices[0].message)

# ✅ 定义两个模拟工具的实现
def get_weather(city):
    return {
        "city": city,
        "temperature": "22°C",
        "condition": "晴",
        "pm2_5": 45
    }

def get_time(city):
    return {
        "city": city,
        "time": "2025-04-09 15:30",
        "timezone": "UTC+8"
    }

# ✅ 逐个执行 tool call 并返回结果
for call in tool_calls:
    tool_name = call.function.name
    args = json.loads(call.function.arguments)

    # 执行对应函数
    if tool_name == "get_weather":
        result = get_weather(args["city"])
    elif tool_name == "get_time":
        result = get_time(args["city"])
    else:
        result = {"error": "未知工具"}

    # 返回结果给模型
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "name": tool_name,
        "content": json.dumps(result)
    })

# ✅ 第二次调用：模型整合 tool 的返回内容，生成最终回答
final_response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=messages
)

print("最终回答：", final_response.choices[0].message.content)
