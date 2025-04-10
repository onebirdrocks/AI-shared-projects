# toolcall-handler

> A unified utility to handle function/tool calls from OpenAI and Claude (Anthropic) models.  
Compatible with OpenAI tool_calling, legacy function_call, and Claude's tool_calls format.

## 📦 Installation

```bash
npm install toolcall-handler
```

## 🚀 Quick Start

```ts
import { detectToolCallSource, handleToolCalls } from 'toolcall-handler';

const toolHandlers = {
  get_weather: async ({ city }) => ({ city, temperature: '21°C' }),
};

const response = {
  tool_calls: [
    { name: 'get_weather', arguments: { city: 'Shanghai' } },
  ],
};

const { source, calls } = detectToolCallSource(response);

const result = await handleToolCalls(calls, source, toolHandlers, {
  timeoutMs: 3000,
  logger: (msg) => console.log(`[ToolCall] ${msg}`),
});

console.log('Result:', result);
```

## 🔧 API

### detectToolCallSource(response)

Automatically detects if the tool/function call is from OpenAI (new or legacy) or Claude.

### handleToolCalls(calls, source, handlers, options?)

Handles execution of tool calls with timeout and logging.

## 🧪 Example Output

```json
[
  {
    "name": "get_weather",
    "result": {
      "city": "Shanghai",
      "temperature": "21°C"
    }
  }
]
```

## 📜 License

MIT
