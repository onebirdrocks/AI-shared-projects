import json
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# define the function 
functions = [
    {
        "name": "get_weather",
        "description": "根据城市查询当前天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "要查询天气的城市，比如 北京、上海"
                }
            },
            "required": ["city"]
        }
    }
]


# query another info
print("########################")
print("Free Chat:")
query ="你叫什么名字？请简单介绍一下你自己"
messages = [
    {"role": "user", "content": query}
]
print("user query:"+query)

response = client.chat.completions.create(
    model="gpt-4-0613",
    messages=messages,
    functions=functions,
    function_call="auto"
)

message = response.choices[0].message
print("AI response message:")
print(message)



print("########################")
print("Query Weather")
# query weather
query ="今天上海天气怎么样？"
messages = [
    {"role": "user", "content": query}
]
print("user query:"+query)

response = client.chat.completions.create(
    model="gpt-4-0613",
    messages=messages,
    functions=functions,
    function_call="auto"
)

message = response.choices[0].message
print("AI response message:")
print(message)

if message.function_call:
    function_name = message.function_call.name
    arguments = json.loads(message.function_call.arguments)
    print("function_name:")
    print(function_name)
    print("function_call:")
    print(arguments)
    
    # The weather function you defined.
    def get_weather(city):
        fake_weather_data = {
            "上海": {"temperature": "25°C", "condition": "多云", "pm2.5": 32},
            "北京": {"temperature": "22°C", "condition": "晴", "pm2.5": 85},
        }
        return fake_weather_data.get(city, {"error": "没有这个城市的天气信息"})

    result = get_weather(arguments["city"])

    messages.append({
        "role": "function",
        "name": function_name,
        "content": json.dumps(result)
    })

    final_response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[
            {"role": "user", "content": "今天上海天气怎么样？"},
            message,
            messages[-1]
        ]
    )

    print("最终回答：", final_response.choices[0].message.content)
else:
    print("模型直接回答：", message.content)

