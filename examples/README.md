"""gstack-agent 使用示例 - 演示三种方法论"""

# === 示例 1：Office-Hours 6 问法 ===
#
# 场景：你想做一个 AI 笔记工具，自动总结会议录音
#
# 命令：
#   gstack-agent office-hours --auto "我想做一个 AI 会议笔记工具，自动总结录音内容"
#
# 预期输出：
#   1. 问题本质：开会太多看不了回放？还是笔记没人写？还是笔记写完没人看？
#   2. 当前怎么做：手动记？Otter.ai？会议结束自己写？
#   3. 失败代价：做了没人用？录音隐私泄露？
#   4. 最小可行解：1周内能交付的最小版本是什么？
#   5. 可证伪条件：什么数据能证明这个方向错了？
#   6. 10倍改进：如果预算×10，会怎么做？

print("[示例 1] 运行：gstack-agent office-hours --auto \"我想做一个 AI 会议笔记工具\"")


# === 示例 2：CEO Review 9 条指令 ===
#
# 场景：你在写技术方案，用 CEO Review 审核
#
# 命令：
#   gstack-agent ceo-review "方案：把所有用户数据从 MongoDB 迁移到 PostgreSQL"
#
# 预期输出：
#   1. 零静默失败：迁移过程中用户报错了吗？
#   2. 错误要有名字：迁移失败时的具体错误信息是什么？
#   3. 数据流阴影路径：空文档、超大文档、特殊字符都处理了吗？
#   4. 边缘情况：迁移中用户新增数据怎么办？
#   5. 可观测性：迁移进度如何监控？
#   6. 必画流程图：迁移步骤图了吗？
#   7. 延迟的必须写下来：数据回滚策略写下来了吗？
#   8. 6个月视角：6个月后这个迁移还合理吗？
#   9. 敢于说放弃：如果迁移成本太高，能不能不迁？

print("\n[示例 2] 运行：gstack-agent ceo-review \"方案：把所有用户数据从 MongoDB 迁移到 PostgreSQL\"")


# === 示例 3：Investigate 4 阶段法 ===
#
# 场景：线上服务挂了
#
# 命令：
#   gstack-agent investigate "生产环境 API 响应时间从 200ms 飙升到 5s，间歇性，凌晨多发"
#
# 预期输出：
#   阶段1：收集症状（错误日志、监控数据、最近变更）
#   阶段2：假设分析（3个假设 + 证据）
#   阶段3：最小验证（加日志、复现、配置检查）
#   阶段4：实施修复（改什么、怎么回滚）

print("\n[示例 3] 运行：gstack-agent investigate \"生产环境 API 响应时间从 200ms 飙升到 5s\"")


# === 示例 4：analyze 全面分析 ===
#
# 场景：完整跑一遍三种方法论
#
# 命令：
#   gstack-agent analyze "我想做一个面向独立开发者的定价工具"

print("\n[示例 4] 运行：gstack-agent analyze \"我想做一个面向独立开发者的定价工具\"")


# === 配置 LLM ===
# 在 ~/.gstack-agent/config.json 中配置：
CONFIG_TEMPLATE = '''{
    "api_key": "sk-xxx",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o"
}'''

print(f"\n[配置] 写入 ~/.gstack-agent/config.json：")
print(CONFIG_TEMPLATE)