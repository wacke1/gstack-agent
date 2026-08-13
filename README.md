# gstack-agent

**把 YC CEO 的思考方法变成你的 AI 助手。**

融合 Garry Tan (YC CEO) 开源的 gstack 框架，将 3 大核心方法论转化为可独立运行的 AI 代理：

| 方法论 | 触发场景 | 核心思想 |
|--------|---------|---------|
| **Office-Hours 6 问法** | 产品构思 / 方案讨论 | 先搞清楚问题，再想方案。问题不清楚，方案就是瞎猜。 |
| **CEO Review 9 条指令** | 方案审核 / 计划评估 | 你不是橡皮图章，让方案变得卓越。 |
| **Investigate 4 阶段法** | 故障排查 / bug 修复 | 没有根因调查就不修。修症状 = 打地鼠。 |

---

## 快速开始

### 安装

```bash
git clone https://github.com/wacke1/gstack-agent.git
cd gstack-agent
pip install -e .
```

### 配置 LLM

在 `~/.gstack-agent/config.json` 中配置：

```json
{
    "api_key": "sk-xxx",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o"
}
```

或通过环境变量：

```bash
export LLM_API_KEY=sk-xxx
export LLM_BASE_URL=https://api.openai.com/v1
export LLM_MODEL=gpt-4o
```

> 支持任意 OpenAI 兼容 API（OpenRouter、Together AI、本地 Ollama 等）。

---

## 用法

### 1. Office-Hours 6 问法 — 搞清问题再想方案

```bash
# 交互模式（推荐）
gstack-agent office-hours "我想做一个 AI 写代码的工具"

# 自动模式（一次性输出完整分析）
gstack-agent office-hours --auto "我想做一个 AI 写代码的工具"
```

6 个问题依次追问：
1. 问题本质是什么？
2. 当前怎么做？代价多少？
3. 失败代价多大？
4. 最小可行解是什么？
5. 怎么证伪？
6. 如果预算×10，怎么做不同的事？

### 2. CEO Review 9 条指令 — 让方案变得卓越

```bash
gstack-agent ceo-review "我的方案：用微服务架构重做整个系统"

# 严格模式
gstack-agent ceo-review --strict "我的方案..."
```

9 条指令逐项审核，不合格的直接指出，不说"可以考虑..."。

### 3. Investigate 4 阶段法 — 没有根因调查就不修

```bash
# 交互模式
gstack-agent investigate "生产环境 API 间歇性 502，凌晨 3 点最多"

# 自动模式
gstack-agent investigate "生产环境 API 间歇性 502"
```

4 阶段：根因调查 → 假设分析 → 最小验证 → 实施修复。

### 4. analyze — 全面分析

```bash
gstack-agent analyze "我想做一个 AI 浏览器插件，自动总结 YouTube 视频"
```

一次性运行全部三种方法论。

---

## 方法论来源

Garry Tan (YC CEO) 的 gstack 框架，开源仓库：https://github.com/garrytan/gstack

---

## 架构

```
gstack-agent/
├── gstack_agent/
│   ├── __init__.py       # 包入口
│   ├── __main__.py       # python -m gstack_agent 入口
│   ├── cli.py            # CLI 入口和参数解析
│   ├── llm.py            # LLM 客户端（OpenAI 兼容 API）
│   ├── office_hours.py   # Office-Hours 6 问法引擎
│   ├── ceo_review.py     # CEO Review 9 条指令引擎
│   └── investigate.py    # Investigate 4 阶段法引擎
├── examples/             # 使用示例
├── tests/                # 测试
├── pyproject.toml        # 项目配置
└── README.md             # 本文件
```

---

## License

MIT