"""立即生成选题和文章大纲"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
from content.generators.topic_generator import generate_topics

# 读取情报包数据
with open('intelligence/daily/2026-11-25-items.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"读取到 {len(items)} 条信息")

# 生成选题
topics = generate_topics(items, top_n=5)

print(f"\n生成 {len(topics)} 个选题：\n")

report = f"""# AI内容选题 | 2026-11-25

**基于情报包生成的可执行选题**

---

"""

for topic in topics:
    report += f"""## 选题{topic['id']}：{topic['title']}

**目标受众**：{topic['audience']}

**核心论点**：{topic['thesis']}

**文章角度**：{topic['angle']}

**素材来源**：
"""
    for mat in topic['materials']:
        report += f"- {mat.get('source', 'unknown')}"
        if mat.get('url'):
            report += f": {mat['url']}"
        if mat.get('type'):
            report += f" ({mat['type']})"
        report += "\n"

    report += f"\n**文章结构**：\n"
    for section in topic['structure']:
        report += f"- {section}\n"

    report += f"\n**预计字数**：{topic['estimated_length']} | **预计耗时**：{topic['estimated_time']}\n\n---\n\n"

# 保存选题
with open('content/topics/2026-11-25.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✓ 选题已保存: content/topics/2026-11-25.md")

# 也保存JSON
with open('content/topics/2026-11-25.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, ensure_ascii=False, indent=2)

print(f"✓ 选题JSON已保存: content/topics/2026-11-25.json")

# 预览
for topic in topics:
    print(f"\n【选题{topic['id']}】{topic['title']}")
    print(f"受众：{topic['audience']}")
    print(f"字数：{topic['estimated_length']} | 耗时：{topic['estimated_time']}")
