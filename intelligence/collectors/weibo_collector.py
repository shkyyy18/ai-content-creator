"""微博热搜采集器"""
import requests
from datetime import datetime
import json

def collect_weibo_hot():
    """采集微博热搜AI相关话题"""
    url = "https://weibo.com/ajax/side/hotSearch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://weibo.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        # AI相关关键词
        ai_keywords = [
            'AI', '人工智能', 'GPT', 'Claude', '大模型',
            '黄仁勋', 'OpenAI', '谷歌', 'Gemini', 'ChatGPT',
            '机器学习', '深度学习', '算法', 'NVIDIA', '芯片',
            'Anthropic', 'DeepMind', '智能体', 'Agent'
        ]

        hot_items = []
        for item in data.get('data', {}).get('realtime', []):
            word = item.get('word', '')

            # 检查是否AI相关
            if any(kw in word for kw in ai_keywords):
                hot_items.append({
                    'title': word,
                    'rank': item.get('rank'),
                    'heat': item.get('num', 0),
                    'url': f"https://s.weibo.com/weibo?q={word}",
                    'source': 'weibo',
                    'timestamp': datetime.now().isoformat(),
                    'category': item.get('category', 'unknown')
                })

        return {
            'success': True,
            'count': len(hot_items),
            'items': hot_items,
            'collected_at': datetime.now().isoformat()
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'items': [],
            'collected_at': datetime.now().isoformat()
        }

if __name__ == '__main__':
    result = collect_weibo_hot()
    print(json.dumps(result, ensure_ascii=False, indent=2))
