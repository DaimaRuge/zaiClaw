# Claude Code CLI 插件与技能报告

> 生成时间：2026-03-29 13:17 | Claude Code 版本：2.1.77

---

## 📦 已安装插件（Plugins）— 26 个，全部已启用

### 🔧 官方插件（claude-plugins-official）— 20 个

| 插件 | 版本 | 功能说明 |
|------|------|----------|
| agent-sdk-dev | b10b583 | Agent SDK 开发调试工具 |
| claude-code-setup | 1.0.0 | Claude Code 初始化配置向导 |
| claude-md-management | 1.0.0 | CLAUDE.md 文件模板管理 |
| code-review | b10b583 | 代码审查与改进建议 |
| commit-commands | b10b583 | Git 提交命令增强 |
| context7 | b10b583 | 第三方库文档上下文注入 |
| explanatory-output-style | b10b583 | 解释性输出风格 |
| feature-dev | b10b583 | 功能开发工作流 |
| figma | 2.0.2 | Figma 设计稿读取与代码生成 |
| frontend-design | b10b583 | 前端 UI/UX 设计辅助 |
| github | b10b583 | GitHub PR/Issue/CI 集成 |
| microsoft-docs | 0.3.1 | Microsoft Learn 官方技术文档 |
| playwright | b10b583 | Playwright 浏览器自动化测试 |
| plugin-dev | b10b583 | 插件开发脚手架工具 |
| remember | 0.1.0 | 会话记忆持久化 |
| skill-creator | b10b583 | 技能/Skill 创建工具 |
| superpowers | 5.0.5 | 综合能力增强包 |
| vercel | 2e79fc9 | Vercel 部署集成 |
| zoominfo | 1.0.1 | ZoomInfo 商业情报查询 |

### 🧩 第三方插件 — 6 个

| 插件 | 版本 | 来源 | 功能说明 |
|------|------|------|----------|
| claude-mem | 10.6.2 | thedotmack | 长期记忆搜索与召回 |
| everything-claude-code | 1.9.0 | affaan-m | Claude Code 全能增强 |
| glm-plan-bug | 0.0.1 | zai-coding-plugins | GLM 规划与 Bug 修复 |
| glm-plan-usage | 0.0.1 | zai-coding-plugins | GLM 用量统计 |
| ui-ux-pro-max | 2.5.0 | nextlevelbuilder | UI/UX 专业设计增强 |

---

## 🔌 MCP 服务器列表 — 14 个

### ✅ 已连接（Connected）— 9 个

| 名称 | 类型 | 端点 | 功能说明 |
|------|------|------|----------|
| microsoft-docs | HTTP | `https://learn.microsoft.com/api/mcp` | Microsoft 官方技术文档查询 |
| context7 | stdio | `npx -y @upstash/context7-mcp` | 第三方库 API 文档上下文 |
| playwright | stdio | `npx @playwright/mcp@latest` | 浏览器自动化与测试 |
| claude-mem | stdio | `~/.claude/plugins/cache/.../mcp-server.cjs` | 本地长期记忆搜索 |
| web-reader | HTTP | `https://api.z.ai/api/mcp/web_reader/mcp` | 网页内容提取 |
| web-search-prime | HTTP | `https://api.z.ai/api/mcp/web_search_prime/mcp` | 网络搜索 |
| zai-mcp-server | stdio | `npx -y @z_ai/mcp-server` | Z.AI 综合服务 |
| zread | HTTP | `https://api.z.ai/api/mcp/zread/mcp` | 文档阅读器 |
| MiniMax | stdio | `uvx minimax-coding-plan-mcp -y` | MiniMax 编码规划 |

### ⚠️ 需要认证（Needs Auth）— 2 个

| 名称 | 端点 | 认证方式 |
|------|------|----------|
| figma | `https://mcp.figma.com/mcp` | OAuth 授权 |
| vercel | `https://mcp.vercel.com` | OAuth / Vercel CLI 登录 |

### ❌ 连接失败（Failed）— 3 个

| 名称 | 端点 | 失败原因 |
|------|------|----------|
| zoominfo | `https://mcp.zoominfo.com/mcp` | 需要 ZoomInfo API Key |
| github | `https://api.githubcopilot.com/mcp/` | 需要 GitHub Copilot 订阅认证 |
| openclaw | `http://localhost:18789/acp` | MCP 协议兼容性问题 |

---

## 📊 统计概览

| 类别 | 数量 | 状态 |
|------|------|------|
| 已安装插件 | 26 | 全部已启用 |
| 官方插件 | 20 | - |
| 第三方插件 | 6 | - |
| MCP 服务器总数 | 14 | - |
| MCP 已连接 | 9 | 64% |
| MCP 需认证 | 2 | 14% |
| MCP 连接失败 | 3 | 21% |

---

## 🔧 待解决问题

### 1. Figma / Vercel 认证

```bash
# Figma 认证
claude mcp auth figma

# Vercel 认证
claude mcp auth vercel
```

### 2. GitHub Copilot MCP

需要有效的 GitHub Copilot 订阅：
```bash
gh auth login
```

### 3. ZoomInfo MCP

如不需要可禁用：
```bash
claude plugins disable zoominfo@claude-plugins-official
```

### 4. OpenClaw MCP

检查 ACP 端点协议兼容性：
```bash
curl http://localhost:18789/acp
openclaw acp
```

---

*报告由 OpenClaw 自动生成*
*GitHub: https://github.com/DaimaRuge/zaiClaw*
