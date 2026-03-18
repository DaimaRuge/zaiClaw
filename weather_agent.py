#!/usr/bin/env python3
"""
weather_agent.py - 天气查询 Agent
基于 s01 核心模式扩展：多工具 + API 调用

核心模式：一个 while 循环 + 一个工具 = 一个 Agent
流程: User → LLM → Tool → tool_result → LLM → ... → 结束
"""

import os
import json
import subprocess
from anthropic import Anthropic
from dotenv import load_dotenv
import urllib.request

load_dotenv(override=True)

# ----------------------------------------
# 1. 初始化客户端和配置
# ----------------------------------------
client = Anthropic()
MODEL = os.environ.get("MODEL_ID", "minimax-portal/MiniMax-M2.7")

SYSTEM = """你是一个天气助手。根据用户需求调用工具查询天气。
可用工具：bash（执行命令）、get_weather（查询天气）
天气数据来源：wttr.in（无需 API key）
回答简洁，包含：温度、天气状况、湿度、风速。"""

# ----------------------------------------
# 2. 工具定义
# ----------------------------------------
TOOLS = [
    {
        "name": "bash",
        "description": "执行 shell 命令",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
    {
        "name": "get_weather",
        "description": "查询指定城市的天气",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称或中文"}
            },
            "required": ["city"],
        },
    }
]

# ----------------------------------------
# 3. 工具实现函数
# ----------------------------------------
def run_bash(command: str) -> str:
    """安全执行 shell 命令"""
    dangerous = ["rm -rf /", "sudo", "shutdown", ">", "/dev/"]
    if any(d in command for d in dangerous):
        return "Error: 命令被拦截"
    try:
        r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return (r.stdout + r.stderr).strip()[:50000] or "(无输出)"
    except subprocess.TimeoutExpired:
        return "Error: 超时 (30s)"

def get_weather(city: str) -> str:
    """使用 wttr.in 查询天气（无需 API key）"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        current = data['current_condition'][0]
        result = f"""📍 {city} 天气预报

🌡️ 温度: {current['temp_C']}°C
🌤️ 天气: {current['weatherDesc'][0]['value']}
💧 湿度: {current['humidity']}%
🌬️ 风速: {current['windspeedKmph']} km/h
🧭 风向: {current['winddir16Point']}
⏰ 更新时间: {current['localObsDateTime']}

未来 3 天:
"""
        for day in data['weather'][:3]:
            result += f"  {day['date']}: {day['maxTempC']}°C ~ {day['minTempC']}°C, {day['hourly'][4]['weatherDesc'][0]['value']}\n"
        return result
    except Exception as e:
        return f"Error: 无法获取天气 - {e}"

# ----------------------------------------
# 4. 核心 Agent 循环
# ----------------------------------------
def agent_loop(messages):
    """
    Agent While 循环模式：
    1. LLM(messages, tools) → response
    2. 追加 assistant 消息
    3. 检查 stop_reason，如果不是 tool_use 则结束
    4. 执行工具调用，收集结果
    5. 将结果作为 user 消息追加，回到步骤 1
    """
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})
        
        if response.stop_reason != "tool_use":
            return
        
        results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                print(f"\033[33m[调用工具: {tool_name}]\033[0m")
                
                if tool_name == "bash":
                    output = run_bash(tool_input["command"])
                elif tool_name == "get_weather":
                    output = get_weather(tool_input["city"])
                else:
                    output = f"Unknown tool: {tool_name}"
                
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
                print(output[:300])
        
        messages.append({"role": "user", "content": results})

# ----------------------------------------
# 5. 主程序入口
# ----------------------------------------
if __name__ == "__main__":
    history = []
    print("🌤️ 天气 Agent 已启动 (输入 q 退出)\n")
    
    while True:
        try:
            query = input("\033[36m天气 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        
        history.append({"role": "user", "content": query})
        agent_loop(history)
        
        # 打印最终回复
        for block in history[-1]["content"]:
            if hasattr(block, "text"):
                print(f"\n\033[32m助手:\033[0m {block.text}\n")
