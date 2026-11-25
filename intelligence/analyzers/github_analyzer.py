"""GitHub深度分析 - 对比用户项目与Trending项目"""
import requests
from datetime import datetime

def get_user_repos(username='shkyyy18', exclude=['mi_fitness_data_bridge']):
    """获取用户的GitHub仓库列表"""
    url = f"https://api.github.com/users/{username}/repos"
    headers = {'User-Agent': 'AI-Content-Creator'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        repos = response.json()

        filtered = []
        for repo in repos:
            if repo['name'] not in exclude:
                filtered.append({
                    'name': repo['name'],
                    'description': repo.get('description', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'language': repo.get('language', 'Unknown'),
                    'topics': repo.get('topics', []),
                    'url': repo['html_url'],
                    'updated': repo['updated_at']
                })

        return filtered
    except Exception as e:
        print(f"获取用户仓库失败: {e}")
        return []

def analyze_trending_vs_user(trending_items, user_repos):
    """对比Trending项目与用户项目，生成改进建议"""

    suggestions = []

    # 分析1：技术栈对比
    trending_langs = {}
    for item in trending_items:
        # 从描述中提取可能的技术栈
        desc = item.get('description', '').lower()
        if 'python' in desc:
            trending_langs['Python'] = trending_langs.get('Python', 0) + 1
        if 'typescript' in desc or 'react' in desc or 'next' in desc:
            trending_langs['TypeScript/React'] = trending_langs.get('TypeScript/React', 0) + 1
        if 'rust' in desc:
            trending_langs['Rust'] = trending_langs.get('Rust', 0) + 1
        if 'go' in desc or 'golang' in desc:
            trending_langs['Go'] = trending_langs.get('Go', 0) + 1

    user_langs = {}
    for repo in user_repos:
        lang = repo.get('language', 'Unknown')
        user_langs[lang] = user_langs.get(lang, 0) + 1

    # 建议1：技术栈扩展
    popular_missing = []
    for lang, count in sorted(trending_langs.items(), key=lambda x: x[1], reverse=True)[:3]:
        if lang not in user_langs:
            popular_missing.append(lang)

    if popular_missing:
        suggestions.append({
            'type': '技术栈扩展',
            'priority': 'high',
            'title': f"考虑学习热门技术栈：{', '.join(popular_missing)}",
            'reason': f"Trending项目中{popular_missing[0]}占比最高，但你的项目中还未使用",
            'action': f"建议创建一个{popular_missing[0]}项目，可以是工具类或学习demo"
        })

    # 分析2：项目主题对比
    trending_themes = []
    for item in trending_items:
        desc = (item.get('description', '') + ' ' + item.get('name', '')).lower()
        if 'agent' in desc or 'autonomous' in desc:
            trending_themes.append('AI Agent')
        if 'rag' in desc or 'retrieval' in desc:
            trending_themes.append('RAG')
        if 'vision' in desc or 'image' in desc or 'video' in desc:
            trending_themes.append('计算机视觉')
        if 'chatbot' in desc or 'chat' in desc:
            trending_themes.append('对话系统')

    user_themes = []
    for repo in user_repos:
        desc = (repo.get('description', '') + ' ' + repo.get('name', '')).lower()
        topics = repo.get('topics', [])
        if 'health' in desc or 'fitness' in desc:
            user_themes.append('健康')
        if 'advisor' in desc or 'assistant' in desc:
            user_themes.append('助手')

    # 建议2：热门主题跟进
    hot_themes = list(set(trending_themes))[:3]
    if hot_themes:
        suggestions.append({
            'type': '热门主题跟进',
            'priority': 'medium',
            'title': f"当前热门方向：{', '.join(hot_themes)}",
            'reason': f"Trending中{hot_themes[0]}类项目获得高关注",
            'action': f"可以考虑在现有项目（如health-advisor）中引入{hot_themes[0]}能力"
        })

    # 分析3：项目活跃度
    total_stars = sum(repo['stars'] for repo in user_repos)
    avg_stars = total_stars / len(user_repos) if user_repos else 0

    trending_avg_stars = 0
    for item in trending_items:
        stars = item.get('stars', '0')
        if isinstance(stars, str):
            stars = int(stars.replace(',', '').replace('k', '000').replace('K', '000')) if stars != 'unknown' else 0
        trending_avg_stars += stars
    trending_avg_stars = trending_avg_stars / len(trending_items) if trending_items else 0

    suggestions.append({
        'type': '项目推广',
        'priority': 'low',
        'title': f"你的项目平均{int(avg_stars)}星，Trending平均{int(trending_avg_stars)}星",
        'reason': '提高项目可见度可以获得更多反馈和贡献',
        'action': '建议：完善README、添加demo、发布到社区（ProductHunt/HackerNews/Reddit）'
    })

    return suggestions

def generate_analysis_report(trending_items, suggestions):
    """生成分析报告Markdown"""

    report = f"""# GitHub深度分析 | {datetime.now().strftime('%Y-%m-%d')}

## 🔥 本期Trending亮点

"""

    for i, item in enumerate(trending_items[:5], 1):
        report += f"{i}. **{item.get('name', 'Unknown')}** ({item.get('stars', '0')} stars)\n"
        report += f"   {item.get('description', '')[:100]}\n"
        report += f"   {item.get('url', '')}\n\n"

    report += """
---

## 💡 对比你的项目

"""

    for sug in suggestions:
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        emoji = priority_emoji.get(sug['priority'], '⚪')

        report += f"""
### {emoji} {sug['type']}：{sug['title']}

**原因**：{sug['reason']}

**建议**：{sug['action']}

---
"""

    report += f"""

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return report

if __name__ == '__main__':
    # 测试
    user_repos = get_user_repos()
    print(f"获取到 {len(user_repos)} 个用户仓库")

    # 模拟trending数据
    trending = [
        {'name': 'openai/swarm', 'description': 'Educational framework for multi-agent systems', 'stars': '12000'},
        {'name': 'facebookresearch/llama', 'description': 'Inference code for LLaMA models', 'stars': '45000'},
    ]

    suggestions = analyze_trending_vs_user(trending, user_repos)
    report = generate_analysis_report(trending, suggestions)

    print(report)
