"""
豆包助手API - 官方SDK接入示例
基于火山引擎 Ark Runtime SDK
支持四个功能模式：chat、deep_chat、ai_search、reasoning_search
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

try:
    from volcenginesdkarkruntime import Ark
    from volcenginesdkarkruntime.types import Response as ArkResponse
    HAS_OFFICIAL_SDK = True
except ImportError:
    HAS_OFFICIAL_SDK = False
    print("警告: 未安装官方SDK，请运行: pip install volcenginesdkarkruntime")


class DouBaoAssistantOfficial:
    """豆包助手官方API客户端"""
    
    # 功能模式常量
    FEATURE_CHAT = "chat"
    FEATURE_DEEP_CHAT = "deep_chat"
    FEATURE_AI_SEARCH = "ai_search"
    FEATURE_REASONING_SEARCH = "reasoning_search"
    
    def __init__(self, api_key: str, base_url: str = "https://ark.cn-beijing.volces.com/api/v3"):
        """
        初始化豆包助手客户端（官方SDK）
        
        Args:
            api_key: 火山引擎API Key
            base_url: API端点，默认使用响应式API
        """
        if not HAS_OFFICIAL_SDK:
            raise ImportError("请先安装官方SDK: pip install volcenginesdkarkruntime")
        
        self.api_key = api_key
        self.base_url = base_url
        
        # 初始化客户端
        self.client = Ark(
            base_url=base_url,
            api_key=api_key,
        )
        
        # Beta测试需要的特殊header
        self.beta_header = {"ark-beta-doubao-app": "true"}
    
    def _build_tools_config(self, feature: str, role_description: Optional[str] = None) -> List[Dict]:
        """
        构建工具配置参数
        
        Args:
            feature: 功能模式 (chat/deep_chat/ai_search/reasoning_search)
            role_description: 自定义角色描述（可选）
            
        Returns:
            工具配置列表
        """
        feature_config = {feature: {"type": "enabled"}}
        
        if role_description:
            feature_config[feature]["role_description"] = role_description
        
        tools = [{
            "type": "doubao_app",
            "feature": feature_config,
            "user_location": {
                "type": "approximate",
                "country": "中国"
            }
        }]
        
        return tools
    
    def chat(
        self,
        messages: List[Dict[str, Any]],
        model: str = "doubao-seed-1-6-251015",
        feature: str = "chat",
        role_description: Optional[str] = None,
        stream: bool = True,
        **kwargs
    ) -> Any:
        """
        发送对话请求（官方Responses API）
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "xxx"}]
            model: 模型名称，默认豆包seed模型
            feature: 功能模式
            role_description: 角色描述
            stream: 是否流式输出
            **kwargs: 其他参数
            
        Returns:
            流式迭代器或完整响应
        """
        tools = self._build_tools_config(feature, role_description)
        
        # 构建请求输入
        input_items = []
        for msg in messages:
            if msg["role"] in ["user", "assistant"]:
                input_items.append({
                    "type": "message",
                    "role": msg["role"],
                    "content": [
                        {
                            "type": "input_text",
                            "text": msg["content"]
                        }
                    ]
                })
        
        try:
            response = self.client.responses.create(
                model=model,
                input=input_items,
                tools=tools,
                stream=stream,
                extra_headers=self.beta_header,
                **kwargs
            )
            return response
        except Exception as e:
            return {
                "error": True,
                "message": f"请求失败: {str(e)}",
                "type": type(e).__name__
            }
    
    def simple_chat(
        self, 
        text: str, 
        feature: str = "chat",
        role_description: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        简化的单轮对话接口
        
        Args:
            text: 用户输入
            feature: 功能模式
            role_description: 角色描述
            **kwargs: 其他参数
            
        Returns:
            完整回复文本
        """
        messages = [{"role": "user", "content": text}]
        response = self.chat(messages, feature=feature, role_description=role_description, **kwargs)
        
        if isinstance(response, dict) and response.get("error"):
            return f"错误: {response['message']}"
        
        # 处理流式响应
        full_text = ""
        try:
            for event in response:
                if hasattr(event, 'delta') and event.delta:
                    full_text += event.delta
        except Exception as e:
            return f"流式处理错误: {str(e)}"
        
        return full_text
    
    def streaming_chat(
        self,
        text: str,
        feature: str = "chat",
        role_description: Optional[str] = None,
        callback: Optional[callable] = None,
        **kwargs
    ) -> str:
        """
        流式对话，支持回调
        
        Args:
            text: 用户输入
            feature: 功能模式
            role_description: 角色描述
            callback: 回调函数(chunk) -> None
            **kwargs: 其他参数
            
        Returns:
            完整回复文本
        """
        messages = [{"role": "user", "content": text}]
        response = self.chat(messages, feature=feature, role_description=role_description, stream=True, **kwargs)
        
        if isinstance(response, dict) and response.get("error"):
            if callback:
                callback(f"错误: {response['message']}")
            return f"错误: {response['message']}"
        
        full_text = ""
        try:
            for chunk in response:
                if hasattr(chunk, 'delta') and chunk.delta:
                    full_text += chunk.delta
                    if callback:
                        callback(chunk.delta)
        except Exception as e:
            error_msg = f"流式处理错误: {str(e)}"
            if callback:
                callback(error_msg)
            full_text = error_msg
        
        return full_text


def demo_all_features():
    """演示四个功能模式的差异"""
    
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY")
        print("示例: export ARK_API_KEY='your-api-key-here'")
        return
    
    if not HAS_OFFICIAL_SDK:
        print("错误: 未安装官方SDK，请先安装:")
        print("  pip install volcenginesdkarkruntime")
        return
    
    assistant = DouBaoAssistantOfficial(api_key=api_key)
    
    question = "豆包App可以做什么？"
    
    print("=" * 60)
    print("豆包助手四大功能模式演示")
    print("=" * 60)
    
    # 1. 日常沟通 (chat)
    print("\n[1] 日常沟通 (chat) - 轻量、亲切、自然")
    print("-" * 60)
    result = assistant.simple_chat(
        question,
        feature="chat",
        role_description="你是一个友善的生活助手"
    )
    print(f"回答: {result[:500]}...\n")
    
    # 2. 深度沟通 (deep_chat)
    print("[2] 深度沟通 (deep_chat) - 逻辑严谨、深度解析")
    print("-" * 60)
    result = assistant.simple_chat(
        question,
        feature="deep_chat",
        role_description="你是一个专业的企业分析助手"
    )
    print(f"回答: {result[:500]}...\n")
    
    # 3. 联网搜索 (ai_search)
    print("[3] 联网搜索 (ai_search) - 实时信息、标注来源")
    print("-" * 60)
    result = assistant.simple_chat(
        "最新AI领域的重要新闻有哪些？",
        feature="ai_search",
        role_description="你是一个科技资讯助手"
    )
    print(f"回答: {result[:500]}...\n")
    
    # 4. 边想边搜 (reasoning_search)
    print("[4] 边想边搜 (reasoning_search) - 逻辑链条完整")
    print("-" * 60)
    result = assistant.simple_chat(
        "分析一下大语言模型在教育的应用前景",
        feature="reasoning_search",
        role_description="你是一个教育科技专家"
    )
    print(f"回答: {result[:500]}...\n")


def interactive_mode():
    """交互式对话模式"""
    
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY")
        return
    
    if not HAS_OFFICIAL_SDK:
        print("错误: 请先安装官方SDK")
        return
    
    print("\n豆包助手 - 交互模式")
    print("功能模式: [1]日常 [2]深度 [3]联网 [4]边想边搜")
    print("输入 'quit' 退出\n")
    
    assistant = DouBaoAssistantOfficial(api_key=api_key)
    
    feature_map = {
        "1": ("chat", "日常沟通"),
        "2": ("deep_chat", "深度沟通"),
        "3": ("ai_search", "联网搜索"),
        "4": ("reasoning_search", "边想边搜")
    }
    
    current_feature = "chat"
    current_role = None
    
    while True:
        try:
            user_input = input("\n请选择功能模式 (1-4) 或输入问题: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            # 切换功能模式
            if user_input in feature_map:
                current_feature, feature_name = feature_map[user_input]
                print(f"已切换到: {feature_name}")
                continue
            
            if not user_input:
                continue
            
            print(f"\n[{feature_map.get(current_feature, ('chat',))[1]}] ", end="", flush=True)
            
            # 流式输出
            full_response = assistant.streaming_chat(
                user_input,
                feature=current_feature,
                role_description=current_role,
                callback=lambda chunk: print(chunk, end="", flush=True)
            )
            
        except KeyboardInterrupt:
            print("\n\n中断退出")
            break
        except Exception as e:
            print(f"\n错误: {str(e)}")


if __name__ == "__main__":
    # 检查SDK安装
    if not HAS_OFFICIAL_SDK:
        print("未检测到官方SDK，请先安装:")
        print("  pip install volcenginesdkarkruntime")
        print("\n安装后运行: python doubao_official_demo.py")
    else:
        # 默认运行演示
        demo_all_features()
        
        # 如需交互模式，取消下面注释:
        # interactive_mode()
