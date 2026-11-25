"""立即生成情报包"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime
import json

# 重新采集数据
from intelligence.collectors.weibo_collector import collect_weibo_hot
from intelligence.collectors.github_collector import collect_github_trending
from intelligence.collectors.community_collector import collect_community_data
from intelligence.scorers.heat_scorer import calculate_heat_score, classify_by_heat
from intelligence.processors.dedup import deduplicate_items, merge_by_category

print("开始采集...")
weibo = collect_weibo_hot()
github = collect_github_trending()
community = collect_community_data()

# 汇总
all_items = []
all_items.extend(weibo.get('items', []))
all_items.extend(github.get('items', []))
all_items.extend(community.get('items', []))

print(f"采集到 {len(all_items)} 条数据")

# 计算热度
for item in all_items:
    item['heat_score'] = calculate_heat_score(item)

# 去重
unique_items = deduplicate_items(all_items)
print(f"去重后 {len(unique_items)} 条")

# 分类
classified = classify_by_heat(unique_items)
categorized = merge_by_category(unique_items)

# 生成Markdown
report = f"""# AI情报包 | 2026-11-25

**采集时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}

**本期数据**：
- 总计：{len(unique_items)} 条信息
- 爆炸级热点：{len(classified['explosive'])} 条
- 高热事件：{len(classified['hot'])} 条
- 常规信息：{len(classified['normal'])} 条

---

## 🔥 爆炸级热点（评分>80）

"""

if len(classified['explosive']) > 0:
    for item in classified['explosive'][:5]:
        report += f"""### {item.get('title', item.get('name', '无标题'))}

**来源**：{item.get('source', 'unknown')} | **热度评分**：{item.get('heat_score', 0):.1f}

**链接**：{item.get('url', '')}

"""
        if item.get('description'):
            report += f"**描述**：{item['description']}\n\n"

        report += "---\n\n"
else:
    report += "暂无爆炸级热点\n\n"

report += """## ⭐ 高热事件（评分50-80）

"""

if len(classified['hot']) > 0:
    for item in classified['hot'][:10]:
        report += f"- **{item.get('title', item.get('name', '无标题'))}** ({item.get('source', 'unknown')} | 评分:{item.get('heat_score', 0):.1f})\n"
        report += f"  {item.get('url', '')}\n"
else:
    report += "暂无高热事件\n"

report += f"""

## 📰 常规信息

"""

for item in classified['normal'][:20]:
    title = item.get('title', item.get('name', '无标题'))
    source = item.get('source', 'unknown')
    score = item.get('heat_score', 0)
    url = item.get('url', '')

    report += f"- **{title}** ({source} | 评分:{score:.1f})\n"
    if url:
        report += f"  {url}\n"

report += f"""

---

## 📊 分类统计

"""

for category, items_list in categorized.items():
    if len(items_list) > 0:
        report += f"- **{category}**: {len(items_list)} 条\n"

report += f"""

---

## 📋 详细列表

"""

for i, item in enumerate(unique_items, 1):
    report += f"""### {i}. {item.get('title', item.get('name', '无标题'))}

- **来源**：{item.get('source', 'unknown')}
- **热度评分**：{item.get('heat_score', 0):.1f}
- **链接**：{item.get('url', '')}
"""

    if item.get('description'):
        report += f"- **描述**：{item['description']}\n"

    if item.get('stars'):
        report += f"- **Stars**：{item['stars']}\n"

    if item.get('score'):
        report += f"- **Score**：{item['score']}\n"

    if item.get('comments'):
        report += f"- **评论数**：{item['comments']}\n"

    report += "\n"

report += f"""---

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

# 保存
output_path = 'intelligence/daily/2026-11-25.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n✓ 情报包已生成: {output_path}")
print(f"\n【摘要】")
print(f"爆炸级: {len(classified['explosive'])} 条")
print(f"高热: {len(classified['hot'])} 条")
print(f"常规: {len(classified['normal'])} 条")

# 也保存原始数据
with open('intelligence/daily/2026-11-25-items.json', 'w', encoding='utf-8') as f:
    json.dump(unique_items, f, ensure_ascii=False, indent=2)

print(f"\n✓ 原始数据已保存: intelligence/daily/2026-11-25-items.json")
