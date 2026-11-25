"""立即运行GitHub深度分析"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
from intelligence.analyzers.github_analyzer import get_user_repos, analyze_trending_vs_user, generate_analysis_report

print("=" * 60)
print("GitHub深度分析")
print("=" * 60)

# 读取今天的情报数据
with open('intelligence/daily/2026-11-25-items.json', 'r', encoding='utf-8') as f:
    all_items = json.load(f)

# 筛选GitHub项目
github_items = [item for item in all_items if item.get('source') == 'github_trending']

print(f"\n读取到 {len(github_items)} 个GitHub Trending项目")

# 获取用户仓库
print("\n正在获取你的GitHub仓库...")
user_repos = get_user_repos('shkyyy18', exclude=['mi_fitness_data_bridge'])

if not user_repos:
    print("⚠ 未能获取用户仓库，可能是API限制，使用模拟数据继续")
    user_repos = [
        {'name': 'health-advisor-internal', 'stars': 2, 'language': 'Python'},
        {'name': 'ai-work', 'stars': 1, 'language': 'Python'}
    ]

print(f"✓ 获取到 {len(user_repos)} 个仓库")

# 生成对比分析
print("\n正在分析...")
suggestions = analyze_trending_vs_user(github_items, user_repos)

# 生成报告
report = generate_analysis_report(github_items, suggestions)

# 保存
output_path = 'intelligence/analysis/2026-11-25-github.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n✓ 分析报告已保存: {output_path}")
print(f"\n生成了 {len(suggestions)} 条改进建议：")

for i, sug in enumerate(suggestions, 1):
    priority_map = {'high': '🔴高', 'medium': '🟡中', 'low': '🟢低'}
    priority = priority_map.get(sug['priority'], '⚪')
    print(f"\n{i}. [{priority}] {sug['type']}：{sug['title']}")
    print(f"   {sug['action']}")

print("\n" + "=" * 60)
