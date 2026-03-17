# 豆包助手API Python接入方案

## 方案概述

本方案提供火山引擎豆包助手API的Python接入实现，包含非流式和流式两种调用方式，支持多轮对话和角色设定。

## 安装前准备

### 1. 获取API Key

1. 访问 [火山引擎控制台](https://www.volcengine.com/)
2. 注册/登录账号
3. 进入"火山方舟"或"AI服务"页面
4. 创建应用并获取API Key
5. 开通豆包助手服务

### 2. 安装依赖

```bash
pip install -r requirements-doubao.txt
```

## 项目结构

```
.
├── doubao_demo.py           # 基础非流式对话示例
├── doubao_stream_demo.py    # 流式对话示例 + CLI交互界面
├── requirements-doubao.txt  # Python依赖包
└── README_DOUBAO.md         # 本说明文档
```

## 快速开始

### 方式一：非流式对话（简单）

```python
from doubao_demo import DouBaoAssistant

# 配置API Key
api_key = "your-api-key-here"

# 创建客户端
assistant = DouBaoAssistant(api_key=api_key)

# 单轮对话
response = assistant.simple_chat("你好，今天天气怎么样？")
print(response)

# 多轮对话
history = [
    {"role": "user", "content": "我喜欢编程"},
    {"role": "assistant", "content": "那太好了！编程是一项很有创造性的技能。"}
]
reply = assistant.multi_turn_chat(history, "你推荐我学什么语言？")
print(reply)
```

### 方式二：流式对话（实时输出）

```python
from doubao_stream_demo import DouBaoStreamAssistant

assistant = DouBaoStreamAssistant(api_key=api_key)

messages = [{"role": "user", "content": "写一个Python Hello World"}]

# 流式输出
for chunk in assistant.stream_chat(messages):
    print(chunk, end="", flush=True)
```

### 方式三：交互式CLI

```bash
# 设置环境变量
export DOUBAO_API_KEY="your-api-key-here"  # Linux/Mac
# 或 Windows: set DOUBAO_API_KEY=your-api-key-here

# 运行交互式对话
python doubao_stream_demo.py
```

## 核心API功能总结

根据火山引擎豆包助手文档，主要功能包括：

### 1. **对话生成 (Chat Completion)**
- 支持单轮和多轮对话
- 可设置系统角色（system messages）
- 支持流式（stream）和非流式输出
- 支持temperature等参数控制生成风格

### 2. **模型配置**
- 支持选择不同豆包模型版本
- 可通过`model`参数指定模型ID（如 `ep-20250228162907-p1bl6`）
- 默认提供豆包助手专用模型

### 3. **参数控制**
- `temperature`：控制随机性，范围0-1，值越大越随机
- `max_tokens`：限制最大输出token数
- 支持其他OpenAI兼容参数

### 4. **多模态支持**（如文档所示）
- 支持文本输入
- 可扩展支持图片等多模态输入
- 支持文档解析和理解

### 5. **应用场景**
- 智能问答
- 文本生成
- 代码编程
- 内容创作
- 知识检索

### 6. **企业级特性**
- 高可用、低延迟
- 数据安全（火山引擎私有化部署支持）
- 灵活的API配额管理
- 监控和日志功能

### 7. **开发友好**
- RESTful API设计
- 兼容OpenAI SDK格式（便于迁移）
- 详细的错误码和状态码
- 完善的SDK支持（Python/Java/Node.js等）

## 高级用法示例

### 自定义参数

```python
result = assistant.chat(
    messages=messages,
    temperature=0.3,      # 更确定性的输出
    max_tokens=1024,      # 限制输出长度
    top_p=0.8,           # 核采样参数
    presence_penalty=0.1  # 话题新鲜度
)
```

### 角色扮演

```python
messages = [
    {"role": "system", "content": "你是一个专业的Python技术专家，请用专业但易懂的方式回答。"},
    {"role": "user", "content": "解释一下Python的装饰器"}
]
```

### 错误处理

```python
result = assistant.chat(messages)
if "error" in result:
    print(f"错误: {result['message']}")
    if result.get('status_code') == 401:
        print("API Key无效，请检查")
    elif result.get('status_code') == 429:
        print("请求频率超限，请稍后重试")
```

## 注意事项

1. **API Key安全**：不要将API Key硬编码在代码中，建议使用环境变量
2. **Token限制**：注意单次请求的max_tokens设置，避免费用超支
3. **异常处理**：网络请求可能失败，务必添加异常处理逻辑
4. **历史管理**：多轮对话时注意管理历史记录长度，避免上下文超限
5. **成本控制**：豆包API按调用计费，生产环境建议添加用量监控

## 常见问题

### Q: 如何查看API剩余配额？
A: 在火山引擎控制台的"用量管理"页面查看。

### Q: 流式和非流式有什么区别？
A: 流式实时返回生成内容，用户体验更好但处理稍复杂；非流式等待完整结果后一次性返回。

### Q: 支持哪些模型？
A: 豆包提供多种模型，详见火山引擎文档，API中通过`model`参数指定。

### Q: 如何实现文件上传和图片理解？
A: 豆包支持多模态输入，需要将文件转为base64或使用其他上传方式，参考官方文档的多模态API章节。

## 参考资源

- [官方文档](https://www.volcengine.com/docs/82379/1978533)
- 火山引擎控制台：https://console.volcengine.com/
- Python SDK：`pip install volcengine-python-sdk`（官方SDK）

## 版本信息

- 本demo基于豆包助手API v3版本设计
- 适配Python 3.8+
- 最后更新：2025-02-28（根据文档最近更新时间）

---

**注意**：实际API端点、模型ID等细节请以火山引擎官方最新文档为准。本方案基于公开信息整理，如有变更请参考官方文档更新。
