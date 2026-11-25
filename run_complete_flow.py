"""完整流程 - 一键生成所有内容"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
import json

print("=" * 60)
print("AI内容创作系统 - 完整流程")
print("=" * 60)

# === 步骤1：采集数据 ===
print("\n【1/4】数据采集中...")

from intelligence.collectors.weibo_collector import collect_weibo_hot
from intelligence.collectors.github_collector import collect_github_trending
from intelligence.collectors.community_collector import collect_community_data

weibo = collect_weibo_hot()
github = collect_github_trending()
community = collect_community_data()

all_items = []
all_items.extend(weibo.get('items', []))
all_items.extend(github.get('items', []))
all_items.extend(community.get('items', []))

print(f"✓ 采集完成：{len(all_items)} 条信息")

# === 步骤2：分析处理 ===
print("\n【2/4】分析处理中...")

from intelligence.scorers.heat_scorer import calculate_heat_score, classify_by_heat
from intelligence.processors.dedup import deduplicate_items, merge_by_category

for item in all_items:
    item['heat_score'] = calculate_heat_score(item)

unique_items = deduplicate_items(all_items)
classified = classify_by_heat(unique_items)
categorized = merge_by_category(unique_items)

print(f"✓ 去重后：{len(unique_items)} 条")
print(f"✓ 爆炸级：{len(classified['explosive'])} | 高热：{len(classified['hot'])} | 常规：{len(classified['normal'])}")

# === 步骤3：生成情报包 ===
print("\n【3/4】生成情报包...")

from generate_report_now import generate_intelligence_report

report_md = f"""# AI情报包 | {datetime.now().strftime('%Y-%m-%d')}

**采集时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}

**本期数据**：
- 总计：{len(unique_items)} 条信息
- 爆炸级热点：{len(classified['explosive'])} 条
- 高热事件：{len(classified['hot'])} 条
- 常规信息：{len(classified['normal'])} 条

---

"""

# 爆炸级
report_md += "## 🔥 爆炸级热点（评分>80）\n\n"
if classified['explosive']:
    for item in classified['explosive'][:5]:
        title = item.get('title', item.get('name', '无标题'))
        report_md += f"### {title}\n\n"
        report_md += f"**来源**：{item.get('source')} | **热度**：{item.get('heat_score', 0):.1f}\n\n"
        report_md += f"{item.get('url', '')}\n\n---\n\n"
else:
    report_md += "暂无爆炸级热点\n\n"

# 高热
report_md += "## ⭐ 高热事件（评分50-80）\n\n"
if classified['hot']:
    for item in classified['hot'][:10]:
        title = item.get('title', item.get('name', '无标题'))
        report_md += f"- **{title}** ({item.get('source')} | {item.get('heat_score', 0):.1f})\n"
else:
    report_md += "暂无高热事件\n\n"

# 常规
report_md += "\n## 📰 常规信息\n\n"
for item in classified['normal'][:20]:
    title = item.get('title', item.get('name', '无标题'))
    report_md += f"- **{title}** ({item.get('source')} | {item.get('heat_score', 0):.1f})\n"

# 保存情报包
today = datetime.now().strftime('%Y-%m-%d')
with open(f'intelligence/daily/{today}.md', 'w', encoding='utf-8') as f:
    f.write(report_md)

print(f"✓ 情报包已保存：intelligence/daily/{today}.md")

# === 步骤4：生成选题 ===
print("\n【4/4】生成选题...")

from content.generators.topic_generator import generate_topics

topics = generate_topics(unique_items, top_n=5)

topics_md = f"# AI内容选题 | {today}\n\n**基于情报包生成的可执行选题**\n\n---\n\n"

for topic in topics:
    topics_md += f"## 选题{topic['id']}：{topic['title']}\n\n"
    topics_md += f"**目标受众**：{topic['audience']}\n\n"
    topics_md += f"**核心论点**：{topic['thesis']}\n\n"
    topics_md += f"**预计字数**：{topic['estimated_length']} | **预计耗时**：{topic['estimated_time']}\n\n"
    topics_md += "---\n\n"

with open(f'content/topics/{today}.md', 'w', encoding='utf-8') as f:
    f.write(topics_md)

print(f"✓ 选题已保存：content/topics/{today}.md")

# === 额外：GitHub深度分析 ===
print("\n【额外】GitHub深度分析...")

try:
    from intelligence.analyzers.github_analyzer import get_user_repos, analyze_trending_vs_user, generate_analysis_report

    user_repos = get_user_repos('shkyyy18', exclude=['mi_fitness_data_bridge'])
    github_items = [item for item in unique_items if item.get('source') == 'github_trending']

    if user_repos and github_items:
        suggestions = analyze_trending_vs_user(github_items, user_repos)
        analysis_report = generate_analysis_report(github_items, suggestions)

        with open(f'intelligence/analysis/{today}-github.md', 'w', encoding='utf-8') as f:
            f.write(analysis_report)

        print(f"✓ GitHub分析已保存：intelligence/analysis/{today}-github.md")
        print(f"  - 生成 {len(suggestions)} 条改进建议")
    else:
        print("⚠ GitHub数据不足，跳过深度分析")
except Exception as e:
    print(f"⚠ GitHub分析失败：{e}")

# === 完成总结 ===
print("\n" + "=" * 60)
print("✅ 全部完成！")
print("=" * 60)
print(f"\n📊 数据统计：")
print(f"  - 采集：{len(all_items)} 条原始数据")
print(f"  - 去重：{len(unique_items)} 条唯一信息")
print(f"  - 选题：{len(topics)} 个可执行选题")
print(f"\n📄 生成文件：")
print(f"  - intelligence/daily/{today}.md")
print(f"  - content/topics/{today}.md")
print(f"  - intelligence/analysis/{today}-github.md (如成功)")
print("\n✨ 下一步：根据选题创作文章\n")
