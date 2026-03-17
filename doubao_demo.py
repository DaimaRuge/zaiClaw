"""
豆包助手API接入示例 - 主程序
基于火山引擎豆包助手API的非流式调用示例
"""

import os
import json
import requests
from typing import Optional, Dict, Any
from datetime import datetime

class DouBaoAssistant:
    """豆包助手API客户端"""
    
    def __init__(self, api_key: str, model: str = "ep-20250228162907-p1bl6"):
        """
        初始化豆包助手客户端
        
        Args:
            api_key: 火山引擎API Key
            model: 模型ID，默认为豆包助手模型
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self, 
        messages: list, 
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> Dict[str, Any]:
        """
        非流式对话
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "xxx"}]
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成token数
            **kwargs: 其他参数
            
        Returns:
            API响应字典
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"请求失败: {str(e)}",
                "status_code": getattr(e.response, 'status_code', None)
            }
    
    def simple_chat(self, text: str) -> str:
        """
        简化的单轮对话接口
        
        Args:
            text: 用户输入文本
            
        Returns:
            助手回复文本
        """
        messages = [{"role": "user", "content": text}]
        result = self.chat(messages)
        
        if "error" in result:
            return f"错误: {result.get('message', '未知错误')}"
        
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "响应格式错误"
    
    def multi_turn_chat(self, history: list, new_message: str) -> str:
        """
        多轮对话接口
        
        Args:
            history: 历史消息列表 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
            new_message: 新消息
            
        Returns:
            助手回复
        """
        messages = history + [{"role": "user", "content": new_message}]
        result = self.chat(messages)
        
        if "error" in result:
            return f"错误: {result.get('message', '未知错误')}"
        
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "响应格式错误"


def main():
    """主函数示例"""
    
    # 从环境变量获取API Key（推荐方式）
    api_key = os.getenv("DOUBAO_API_KEY")
    
    if not api_key:
        print("请设置环境变量 DOUBAO_API_KEY 或直接在代码中填入你的API Key")
        print("示例: export DOUBAO_API_KEY='your-api-key-here'")
        return
    
    # 创建客户端
    assistant = DouBaoAssistant(api_key=api_key)
    
    # 示例1: 单轮对话
    print("=" * 50)
    print("示例1: 单轮对话")
    response = assistant.simple_chat("你好，请介绍一下你自己")
    print(f"助手: {response}")
    
    # 示例2: 多轮对话
    print("\n" + "=" * 50)
    print("示例2: 多轮对话")
    
    history = [
        {"role": "user", "content": "用一句话描述北京"},
        {"role": "assistant", "content": "北京是中国的首都，是一座有着三千年历史的古都。"}
    ]
    
    new_response = assistant.multi_turn_chat(history, "那上海呢？")
    print(f"助手: {new_response}")
    
    # 示例3: 系统角色设定
    print("\n" + "=" * 50)
    print("示例3: 带系统角色的对话")
    
    messages = [
        {"role": "system", "content": "你是一个专业的Python编程助手，擅长解答技术问题。"},
        {"role": "user", "content": "请用五行代码实现一个快速排序算法"}
    ]
    
    result = assistant.chat(messages)
    if "error" not in result:
        print(f"助手: {result['choices'][0]['message']['content']}")


if __name__ == "__main__":
    main()
