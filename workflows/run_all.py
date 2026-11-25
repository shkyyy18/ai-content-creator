"""AI内容创作系统主流程"""
import sys
import os
from datetime import datetime
import json

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def generate_intelligence_report(items, classified, categorized, date):
    """生成情报包Markdown"""

    report = f"""# AI情报包 | {date}

**采集时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}

**本期数据**：
- 总计：{len(items)} 条信息
- 爆炸级热点：{len(classified['explosive'])} 条
- 高热事件：{len(classified['hot'])} 条
- 常规信息：{len(classified['normal'])} 条

---

## 🔥 爆炸级热点（评分>80）

"""

    for item in classified['explosive'][:5]:
        report += f"""### {item.get('title', '无标题')}

**来源**：{item.get('source', 'unknown')} | **热度评分**：{item.get('heat_score', 0):.1f}

**链接**：{item.get('url', '')}

---

"""

    if len(classified['explosive']) == 0:
        report += "暂无爆炸级热点\n\n"

    report += """## ⭐ 高热事件（评分50-80）

"""

    for item in classified['hot'][:10]:
        report += f"- **{item.get('title', '无标题')}** ({item.get('source', 'unknown')} | 评分:{item.get('heat_score', 0):.1f})\n"

    report += f"""

---

## 📊 分类统计

"""

    for category, items_list in categorized.items():
        if len(items_list) > 0:
            report += f"- **{category}**: {len(items_list)} 条\n"

    report += f"""

---

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return report

def run_full_pipeline():
    """执行完整流程"""
    start_time = datetime.now()
    today = start_time.strftime('%Y-%m-%d')

    print(f"=== AI内容创作系统 ===")
    print(f"开始时间: {start_time.strftime('%H:%M:%S')}")
    print(f"目标日期: {today}")
    print()

    results = {
        'date': today,
        'start_time': start_time.isoformat(),
        'steps': []
    }

    # === 阶段1：数据采集（15分钟） ===
    print("【阶段1/3】数据采集...")

    # 1.1 微博热搜
    print("  [1/6] 采集微博热搜...")
    try:
        from intelligence.collectors.weibo_collector import collect_weibo_hot
        weibo_result = collect_weibo_hot()
        results['steps'].append({
            'name': 'weibo',
            'success': weibo_result['success'],
            'count': weibo_result['count']
        })
        print(f"      ✓ 成功采集 {weibo_result['count']} 条")
    except Exception as e:
        print(f"      ✗ 失败: {e}")
        results['steps'].append({'name': 'weibo', 'success': False, 'error': str(e)})

    # 1.2 GitHub Trending
    print("  [2/6] 采集GitHub Trending...")
    try:
        from intelligence.collectors.github_collector import collect_github_trending
        github_result = collect_github_trending()
        results['steps'].append({
            'name': 'github',
            'success': github_result['success'],
            'count': github_result['count']
        })
        print(f"      ✓ 成功采集 {github_result['count']} 个项目")
    except Exception as e:
        print(f"      ✗ 失败: {e}")
        results['steps'].append({'name': 'github', 'success': False, 'error': str(e)})

    # 1.3 Twitter (Nitter)
    print("  [3/6] 采集Twitter (Nitter镜像)...")
    try:
        from intelligence.collectors.nitter_collector import collect_twitter_via_nitter
        twitter_accounts = ['sama', 'ylecun', 'karpathy']
        twitter_result = collect_twitter_via_nitter(twitter_accounts)
        results['steps'].append({
            'name': 'twitter',
            'success': twitter_result['success'],
            'count': twitter_result['count']
        })
        print(f"      ✓ 成功采集 {twitter_result['count']} 条推文")
    except Exception as e:
        print(f"      ✗ 失败: {e}")
        results['steps'].append({'name': 'twitter', 'success': False, 'error': str(e)})

    # 1.4 投融资
    print("  [4/6] 采集投融资数据...")
    try:
        from intelligence.collectors.funding_collector import collect_funding_data
        funding_result = collect_funding_data()
        results['steps'].append({
            'name': 'funding',
            'success': funding_result['success'],
            'count': funding_result['count']
        })
        print(f"      ✓ 成功采集 {funding_result['count']} 条")
    except Exception as e:
        print(f"      ✗ 失败: {e}")
        results['steps'].append({'name': 'funding', 'success': False, 'error': str(e)})

    # 1.5 社区讨论
    print("  [5/6] 采集社区讨论...")
    try:
        from intelligence.collectors.community_collector import collect_community_data
        community_result = collect_community_data()
        results['steps'].append({
            'name': 'community',
            'success': community_result['success'],
            'count': community_result['count']
        })
        print(f"      ✓ 成功采集 {community_result['count']} 条")
    except Exception as e:
        print(f"      ✗ 失败: {e}")
        results['steps'].append({'name': 'community', 'success': False, 'error': str(e)})

    # 1.6 公众号（暂时跳过）
    print("  [6/6] 采集公众号文章...")
    print("      ⚠ 待实现浏览器自动化")

    # 汇总所有采集数据
    all_items = []
    if weibo_result.get('success'):
        all_items.extend(weibo_result.get('items', []))
    if github_result.get('success'):
        all_items.extend(github_result.get('items', []))
    if 'funding_result' in locals() and funding_result.get('success'):
        all_items.extend(funding_result.get('items', []))
    if 'community_result' in locals() and community_result.get('success'):
        all_items.extend(community_result.get('items', []))

    results['total_items'] = len(all_items)
    print()

    # === 阶段2：分析处理（15分钟） ===
    print("【阶段2/3】分析处理...")

    # 2.1 热度评分与去重
    print("  [1/3] 热度评分与去重...")
    try:
        from intelligence.scorers.heat_scorer import classify_by_heat
        from intelligence.processors.dedup import deduplicate_items, merge_by_category

        # 去重
        unique_items = deduplicate_items(all_items)

        # 热度分类
        classified = classify_by_heat(unique_items)

        # 按类别分组
        categorized = merge_by_category(unique_items)

        results['analysis'] = {
            'total_unique': len(unique_items),
            'explosive': len(classified['explosive']),
            'hot': len(classified['hot']),
            'normal': len(classified['normal']),
            'by_category': {k: len(v) for k, v in categorized.items()}
        }

        print(f"      ✓ 去重后 {len(unique_items)} 条")
        print(f"      ✓ 爆炸级 {len(classified['explosive'])} 条")
        print(f"      ✓ 高热 {len(classified['hot'])} 条")

    except Exception as e:
        print(f"      ✗ 分析失败: {e}")
        results['analysis'] = {'error': str(e)}

    # 2.2 生成情报包
    print("  [2/3] 生成情报包...")
    try:
        output_md = generate_intelligence_report(unique_items, classified, categorized, today)

        # 保存Markdown
        md_path = os.path.join(output_dir, f'{today}.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(output_md)

        print(f"      ✓ 情报包已生成: {md_path}")

    except Exception as e:
        print(f"      ✗ 生成失败: {e}")

    # 2.3 GitHub深度分析（暂时跳过）
    print("  [3/3] GitHub深度分析...")
    print("      ⚠ 需要读取用户项目，待下轮实现")

    print()

    # === 阶段3：内容创作（15分钟） ===
    print("【阶段3/3】内容创作...")
    print("  [1/3] 生成选题...")
    print("      ⚠ 待实现（需要Claude API）")
    print("  [2/3] 创作文章...")
    print("      ⚠ 待实现（需要风格模板）")
    print("  [3/3] 质量检查...")
    print("      ⚠ 待实现")
    print()

    # === 完成 ===
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    results['end_time'] = end_time.isoformat()
    results['duration_seconds'] = duration

    print("=" * 50)
    print(f"✓ 全流程完成")
    print(f"耗时: {int(duration // 60)}分{int(duration % 60)}秒")
    print(f"结果保存至: intelligence/daily/{today}.json")

    # 保存结果
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'intelligence', 'daily')
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, f'{today}.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results

if __name__ == '__main__':
    run_full_pipeline()
