"""Investigate 4 阶段故障排查 - 没有根因调查就不修"""
from .llm import LLMClient

PROMPT_TEMPLATE = """你是 Garry Tan (YC CEO) 的 Investigate 助手。

故障排查时，没有根因调查就不修。修症状 = 打地鼠。

## 4 阶段强制流程：

### 阶段 1：根因调查（只观察，不修改）
1. 收集症状：读错误信息、堆栈、复现步骤
2. 读代码：从症状追溯到可能原因
3. 查近期变更：git log --oneline -20。回归 = 根因在 diff 里
4. 复现：能稳定触发吗？不能就继续收集证据
5. 查历史：同一区域的反复 bug 是架构异味

输出：根因假设（具体、可验证的声明）

### 阶段 2：假设分析
列出 3 个假设 + 每个的证据（支持/反对）
- 竞态条件（间歇性、时序相关）
- nil/null 传播（缺守卫）
- 状态损坏（不一致数据）
- 集成故障（超时、外部 API）
- 配置漂移（本地行、生产挂）
- 缓存过期（旧数据，清缓存修了）

### 阶段 3：最小验证
1. 在疑似根因处加临时日志/assert
2. 跑复现，看证据是否匹配
3. 假设不对 → 回阶段 1
4. 3 次假设失败 → 停，可能是架构问题

### 阶段 4：实施修复
1. 先备份（git stash / 分支 / 文件拷贝）
2. 修根因，不修症状
3. 写回归测试（无修复时失败，有修复时通过）
4. 跑完整测试
5. 修复 >5 个文件 → 标记爆炸半径

## 交互规则：
- 用户描述症状 → 你按 4 阶段引导
- 每阶段只问一个关键问题
- 不猜不猜不猜

## 症状：
{user_input}
"""


def run_investigate(user_input: str, interactive: bool = False):
    print("\n" + "=" * 60)
    print("🔍 gstack Investigate 4 阶段法")
    print("=" * 60)
    print(f"\n症状：{user_input}")

    if interactive:
        _interactive_investigate(user_input)
    else:
        _auto_investigate(user_input)


def _auto_investigate(user_input: str):
    prompt = PROMPT_TEMPLATE.format(user_input=user_input)
    prompt += "\n\n（自动模式：一次性输出完整的 4 阶段分析报告）"
    client = LLMClient()
    response = client.chat(prompt)
    print("\n--- 调查分析 ---\n")
    print(response)


def _interactive_investigate(user_input: str):
    print("\n[交互模式]\n")
    stages = [
        ("阶段 1：根因调查", "你能提供的症状信息是什么？错误日志、复现步骤、最近改了什么？"),
        ("阶段 2：假设分析", "基于以上信息，你认为最可能的根因是什么？有没有其他可能性？"),
        ("阶段 3：最小验证", "你能通过什么方式验证这个假设？加日志、复现、检查配置？"),
        ("阶段 4：实施修复", "假设验证后，修复方案是什么？改什么、怎么回滚、怎么验证？"),
    ]

    client = LLMClient()
    conversation = [
        {"role": "system", "content": PROMPT_TEMPLATE.format(user_input=user_input)}
    ]

    for name, question in stages:
        print(f"\n{'─' * 40}")
        print(f"  {name}")
        print(f"{'─' * 40}")
        print(f"{question}")
        answer = input("\n你的回答：").strip()
        if not answer:
            print("⚠️  跳过此阶段。")
            answer = "（未回答）"
        conversation.append({"role": "user", "content": f"[{name}] {answer}"})

    print(f"\n{'=' * 60}")
    print("📋 4 阶段调查完成。")
    final = client.chat(conversation + [
        {"role": "user", "content": "基于以上所有回答，给一个完整的调试报告。"}
    ])
    print(final)