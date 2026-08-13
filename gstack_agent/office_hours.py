"""Office-Hours 6 问法 - 先搞清楚问题再想方案"""
from .llm import LLMClient


def build_prompt(user_input: str, auto: bool = False) -> str:
    base = """你是 Garry Tan (YC CEO) 的 Office-Hours 助手，使用他的 6 问法。

方法论：Felix 提出想法时，你逐个追问（一次一个），搞清问题本质再给方案。

## 6 个强制问题（按顺序）：

1. **问题本质** — 这个方案要解决的具体问题是什么？不是表面症状
2. **当前怎么做** — 现有方案的代价（时间/金钱/痛苦）
3. **失败代价** — 最坏情况：时间浪费、机会成本、技术债
4. **最小可行解** — 1周内能交付的最小版本，砍到只剩核心
5. **可证伪条件** — 什么证据能证明这个方案不行？
6. **10倍改进** — 如果预算/时间 ×10，会怎么做不同的事？

## 交互规则：
- 一次只问一个问题
- 用户回答后立刻追问下一个
- 不问模糊问题，只问能推动决策的具体问题
- 问完 6 个问题后，给一个具体行动项，不是一堆策略
- 反奉承：不说"这个思路不错"，直接表态

## 用户想法：
{user_input}"""
    prompt = base.format(user_input=user_input)
    if auto:
        prompt += """

## 输出格式：
第 N 问：{问题名}
{基于现有信息的初步分析 + 追问}

（第 6 问后给出最终行动项）

（自动模式：一次性输出 6 个问题的完整分析，每个问题附带基于现有信息的初步判断）"""
    return prompt


def run_office_hours(user_input: str, auto: bool = False):
    print("\n" + "=" * 60)
    print("🏢 gstack Office-Hours 6 问法")
    print("=" * 60)
    print(f"\n你的想法：{user_input}")

    if auto:
        prompt = build_prompt(user_input, auto=True)
        print("\n[自动分析模式]\n")
        response = LLMClient().chat(prompt)
        print(response)
        return

    _interactive_office_hours(user_input)


def _interactive_office_hours(user_input: str):
    print("\n[交互模式] 我会逐个问你 6 个问题，每个问题只需要回答一个。\n")
    questions = [
        ("问题本质", "你的方案要解决的具体问题是什么？不是表面症状，是最底层的问题。"),
        ("当前怎么做", "现在这个问题是怎么解决的？代价是什么（时间/金钱/痛苦）？"),
        ("失败代价", "如果这个方案做失败了，最坏情况是什么？时间浪费多少？机会成本多大？"),
        ("最小可行解", "1周内能交付的最小版本是什么？砍到只剩最核心的功能。"),
        ("可证伪条件", "什么证据能证明这个方案不行？你需要看到什么数据才能判断对错？"),
        ("10倍改进", "如果预算和时间放大10倍，你会怎么做完全不同的事？"),
    ]

    client = LLMClient()
    conversation = [
        {"role": "system", "content": build_prompt(user_input, auto=False)}
    ]

    for i, (name, question) in enumerate(questions, 1):
        print(f"\n{'─' * 40}")
        print(f"第 {i} 个问题：{name}")
        print(f"{'─' * 40}")
        print(f"{question}")

        answer = input("\n你的回答：").strip()
        if not answer:
            print("⚠️  你跳过了这个问题。")
            answer = "（未回答）"

        conversation.append({"role": "user", "content": f"[第 {i} 问 - {name}] {answer}"})

        followup = client.chat(conversation, max_tokens=100)
        if followup:
            print(f"\n助手回应：{followup.strip()}")

    print(f"\n{'=' * 60}")
    print("📋 6 问完成。基于你的回答，我的判断：")
    print("=" * 60)
    final = client.chat(conversation + [
        {"role": "user", "content": "基于以上所有回答，给一个具体的行动项。直接、可执行，不是一堆策略。"}
    ])
    print(final)
