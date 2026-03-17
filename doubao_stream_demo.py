"""
豆包助手API - 流式对话示例
支持实时流式输出，提升用户体验
"""

import os
import json
import requests
from typing import Optional, Dict, Any, Generator


class DouBaoStreamAssistant:
    """豆包助手流式API客户端"""
    
    def __init__(self, api_key: str, model: str = "ep-20250228162907-p1bl6"):
        """
        初始化流式客户端
        
        Args:
            api_key: 火山引擎API Key
            model: 模型ID
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def stream_chat(
        self, 
        messages: list, 
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        流式对话生成器
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Yields:
            每次流式返回的文本片段
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,  # 开启流式模式
            **kwargs
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            full_content = ""
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                    
                if line.startswith("data: "):
                    data = line[6:]  # 移除 "data: " 前缀
                    
                    if data == "[DONE]":
                        break
                    
                    try:
                        chunk = json.loads(data)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            full_content += content
                            yield content
                    except json.JSONDecodeError:
                        continue
                        
        except requests.exceptions.RequestException as e:
            yield f"\n[错误] 请求失败: {str(e)}"
    
    def chat_with_stream(
        self, 
        messages: list, 
        callback: Optional[callable] = None,
        **kwargs
    ) -> str:
        """
        流式对话，可设置回调函数实时处理
        
        Args:
            messages: 消息列表
            callback: 回调函数，接收每个文本片段
            **kwargs: 其他参数
            
        Returns:
            完整回复文本
        """
        full_response = ""
        
        for chunk in self.stream_chat(messages, **kwargs):
            full_response += chunk
            if callback:
                callback(chunk)
            else:
                print(chunk, end="", flush=True)
        
        return full_response


def interactive_cli():
    """交互式命令行界面"""
    
    api_key = os.getenv("DOUBAO_API_KEY")
    if not api_key:
        print("错误: 请先设置环境变量 DOUBAO_API_KEY")
        return
    
    assistant = DouBaoStreamAssistant(api_key=api_key)
    
    print("豆包助手 - 流式对话模式")
    print("输入 'quit' 或 'exit' 退出")
    print("-" * 50)
    
    history = []
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            if not user_input:
                continue
            
            # 添加用户消息到历史
            history.append({"role": "user", "content": user_input})
            
            # 流式输出回复
            print("助手: ", end="", flush=True)
            assistant_reply = assistant.chat_with_stream(history)
            
            # 添加助手回复到历史
            history.append({"role": "assistant", "content": assistant_reply})
            
            # 保持历史长度，避免token超限
            if len(history) > 20:
                history = history[-20:]
                
        except KeyboardInterrupt:
            print("\n\n检测到中断，退出中...")
            break
        except Exception as e:
            print(f"\n[错误] {str(e)}")


if __name__ == "__main__":
    interactive_cli()
