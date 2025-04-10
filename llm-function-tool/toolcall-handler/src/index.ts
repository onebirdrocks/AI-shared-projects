export type ToolCallSource = "openai" | "claude" | "openai_legacy";

export interface HandlerOptions {
  timeoutMs?: number; // 默认超时时间
  logger?: (message: string) => void; // 可选日志函数
}

export type ToolHandlerMap = Record<string, (args: any) => Promise<any>>;

async function callWithTimeout<T>(fn: () => Promise<T>, timeoutMs: number): Promise<T> {
  return new Promise<T>((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("Function timeout")), timeoutMs);
    fn()
      .then((res) => {
        clearTimeout(timer);
        resolve(res);
      })
      .catch((err) => {
        clearTimeout(timer);
        reject(err);
      });
  });
}

export async function handleToolCalls(
  toolCalls: any[],
  source: ToolCallSource,
  toolHandlers: ToolHandlerMap,
  options: HandlerOptions = {}
) {
  const { timeoutMs = 5000, logger = console.log } = options;
  const results = [];

  for (const call of toolCalls) {
    let name: string;
    let args: any;

    try {
      if (source === "openai") {
        name = call.function.name;
        args = JSON.parse(call.function.arguments);
      } else if (source === "claude") {
        name = call.name;
        args = call.arguments;
      } else if (source === "openai_legacy") {
        name = call.name;
        args = JSON.parse(call.arguments);
      } else {
        throw new Error("Unsupported source type");
      }

      logger(\`🔧 [ToolCall] Invoking "\${name}" with args: \${JSON.stringify(args)}\`);

      const handler = toolHandlers[name];
      if (!handler) {
        logger(\`❌ No handler found for tool: "\${name}"\`);
        results.push({ name, error: "Handler not found" });
        continue;
      }

      const result = await callWithTimeout(() => handler(args), timeoutMs);

      logger(\`✅ [ToolCall] "\${name}" executed successfully. Result: \${JSON.stringify(result)}\`);
      results.push({ name, result });
    } catch (err) {
      logger(\`💥 [ToolCall] "\${call.name || 'unknown'}" failed: \${(err as Error).message}\`);
      results.push({
        name: call.name || "unknown",
        error: (err as Error).message,
      });
    }
  }

  return results;
}

export function detectToolCallSource(response: any): {
  source: ToolCallSource;
  calls: any[];
} {
  if (Array.isArray(response.tool_calls) && response.tool_calls[0]?.name) {
    return { source: "claude", calls: response.tool_calls };
  }
  if (Array.isArray(response.tool_calls) && response.tool_calls[0]?.function?.name) {
    return { source: "openai", calls: response.tool_calls };
  }
  if (response.function_call?.name && response.function_call?.arguments) {
    return { source: "openai_legacy", calls: [response.function_call] };
  }
  return { source: "unknown", calls: [] };
}

// 示例用法
if (require.main === module) {
  (async () => {
    const toolHandlers: ToolHandlerMap = {
      get_weather: async ({ city }) => ({ city, temperature: "21°C" }),
    };

    const response = {
      tool_calls: [
        { name: "get_weather", arguments: { city: "Shanghai" } },
      ],
    };

    const { source, calls } = detectToolCallSource(response);
    const result = await handleToolCalls(calls, source, toolHandlers, {
      timeoutMs: 3000,
      logger: (msg) => console.log(`[ToolCall] ${msg}`),
    });

    console.log("\nFinal result:", JSON.stringify(result, null, 2));
  })();
}
