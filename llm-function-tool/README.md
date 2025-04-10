
# 🌟 OpenAI Function Calling & Tool Calling 学习笔记

> 通过实际代码和问题解答，全面掌掌 `function_call` 与 `tool_call` 的原理、用法与差异。

---

## 🧠 一、什么是 Function Calling？

Function Calling 是 OpenAI 在 2023 年中推出的一项功能，让模型可以调用开发者定义的函数，输出结构化的 `function_call` 响应。

### 🧱 原理
- 开发者定义函数名、描述和参数（用 JSON Schema 表示）
- 模型判断是否调用该函数，并给出调用参数
- 开发者执行函数，返回结果，再交给模型继续回复

### ✅ 使用模型版本
- `gpt-3.5-turbo-0613`
- `gpt-4-0613`
- `gpt-3.5-turbo-1106`（也支持 tool calling）

---

## 🛠 二、什么是 Tool Calling？

Tool Calling 是 Function Calling 的升级版，从 2023 年底 GPT-4 Turbo 起正式引入，支持多工具并发调用。

### 🎯 特点
- 使用 `tools=[...]` 替代 `functions=[...]`
- 支持一次调用多个工具（并发）
- 支持扩展类型，如 function、code_interpreter、retrieval、browser、plugin 等

### ✅ 使用模型版本
- `gpt-4-1106-preview`
- `gpt-4-0125-preview`
- `gpt-3.5-turbo-1106`
- `gpt-4-turbo`

---

## 🆚 三、Function Calling vs Tool Calling 对比表

| 特性               | Function Calling            | Tool Calling（新版）         |
|--------------------|-----------------------------|-------------------------------|
| 参数字段名         | `functions`                 | `tools`                       |
| 响应字段           | `function_call`             | `tool_calls`（支持多个）     |
| 支持并发调用       | ❌                          | ✅                            |
| 支持类型           | 仅 `function`               | `function`、`code`、`plugin` |
| 引入时间           | 2023 年 6 月                | 2023 年 11 月                |
| 推荐使用           | ✅（用于兼容）              | ✅（未来标准）               |

---

## 🧪 四、完整 Tool Calling 示例（含多个工具）

我们定义两个工具：
- `get_weather(city)`：查天气
- `get_time(city)`：查时间

用户输入：“现在北京的天气和时间怎么样？”
→ 模型并发调用两个工具 → 整合结果输出自然语言

👉 示例代码见：[tool-calling-multi-tools-example](#)

---

## 🧾 五、如何判断模型是否支持 function_call/tooling？

### ✅ 官方支持模型判断方法

| 模型                      | function_call | tool_calling |
|---------------------------|---------------|---------------|
| gpt-3.5-turbo-0613        | ✅            | ❌            |
| gpt-4-0613                | ✅            | ❌            |
| gpt-4-1106-preview        | ✅            | ✅            |
| gpt-4-0125-preview        | ✅            | ✅            |
| gpt-3.5-turbo-1106        | ✅            | ✅            |
| gpt-4-turbo               | ✅            | ✅            |

### ✅ 检测方法

#### 方式一：发起调用测试（推荐）

```python
def supports_tool_calling(model: str) -> bool:
    try:
        ...
    except Exception as e:
        return "tools" not in str(e).lower()
```

#### 方式二：维护模型能力表

```python
MODEL_CAPABILITIES = {
  "gpt-4-0613": {"supports_function_call": True, "supports_tool_call": False},
  "gpt-4-1106": {"supports_function_call": True, "supports_tool_call": True},
}
```

---

## 🔍 六、不同角色的作用（role）

| Role         | 作用说明                                           |
|--------------|----------------------------------------------------|
| `system`     | 定义模型的行为和身份（如客服、助手）              |
| `user`       | 用户输入                                           |
| `assistant`  | 模型的输出（也可以包含函数调用请求）              |
| `function`   | 用户执行函数后返回结果（旧版 function calling）   |
| `tool`       | 用户执行工具后返回结果（新版 tool calling）       |

---

## 🌍 七、DeepSeek 等国产模型是否支持 Tool Calling？

目前如 **DeepSeek V3** 这样的模型已支持 Function Calling，部分也支持 Tooling，但取决于所使用的平台与托管方式（如 Fireworks、Cloudflare Workers AI）。

建议关注：
- [DeepSeek 官方 GitHub](https://github.com/deepseek-ai)
- [Fireworks.ai](https://fireworks.ai)

---

## 💡 附：参考工具和库

- [OpenAI 官方 Python SDK](https://github.com/openai/openai-python)
- [LangChain function/tool wrappers](https://docs.langchain.com/)
- [OpenAI Function Calling 文档](https://platform.openai.com/docs/guides/function-calling)
- [OpenAI Tool Calling 文档](https://platform.openai.com/docs/guides/tool-calling)

---

> 学习工具调用的原理，不只是为了用 OpenAI，也能帮助你设计自己的 LLM Agent 架构。
>
> — *onebird, with love.*

