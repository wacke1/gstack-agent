"""CEO Review 9 条核心指令 - 让方案变得卓越"""
from .llm import LLMClient

NINE_DIRECTIVES = [
    "零静默失败：每个失败模式必须可见",
    "错误要有名字：说清具体异常、触发条件、用户看到什么",
    "数据流阴影路径：每个数据流有 happy path + 3 个阴影（nil 输入、空/零长度、上游错误）",
    "边缘情况必问：双击、中途导航、慢连接、过期状态、返回键",
    "可观测性是范围：监控、告警、文档是一等交付物",
    "必画流程图：非简单流程必须有流程图",
    "延迟的必须写下来：模糊的意图 = 谎言",
    "6个月视角：为6个月后的未来优化，不只是今天",
    "敢于说放弃：你有权说「放弃吧，换个方案」",
]

PROMPT_TEMPLATE = """你是 Garry Tan (YC CEO) 的 CEO Review 助手。

用以下 9 条核心指令逐项审核方案，不完美就提出来：

"""

for i, d in enumerate(NINE_DIRECTIVES, 1):
    PROMPT_TEMPLATE += f"{i}. **{d}**\n"

PROMPT_TEMPLATE += """
## 审核要求：
- 每一条指令逐项过，不合格的直接指出
- 不说"可以考虑..."，直接给修改建议
- 最后给一个总评分（1-10分）+ 最重要的 1 个修改建议

## 方案：
{user_input}
"""


def run_ceo_review(user_input: str, strict: bool = False):
    print("\n" + "=" * 60)
    print("📋 gstack CEO Review 9 条指令审核")
    print("=" * 60)
    print(f"\n方案：{user_input}")

    prompt = PROMPT_TEMPLATE.format(user_input=user_input)
    if strict:
        prompt += "\n\n（严格模式：每一项必须 100% 符合，否则标记为 FAIL）"

    client = LLMClient()
    response = client.chat(prompt)
    print("\n--- 审核结果 ---\n")
    print(response)