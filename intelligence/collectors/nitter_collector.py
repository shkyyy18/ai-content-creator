"""Nitter镜像Twitter采集器"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def collect_twitter_via_nitter(accounts, nitter_instance='nitter.net'):
    """通过Nitter镜像采集Twitter动态

    Args:
        accounts: Twitter账号列表（不带@）
        nitter_instance: Nitter镜像站域名
    """
    items = []

    for account in accounts:
        url = f"https://{nitter_instance}/{account}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取推文
            tweets = soup.find_all('div', class_='timeline-item')[:5]  # 最新5条

            for tweet in tweets:
                content_div = tweet.find('div', class_='tweet-content')
                if not content_div:
                    continue

                content = content_div.get_text(strip=True)

                # 过滤AI相关内容
                ai_keywords = ['AI', 'GPT', 'LLM', 'model', 'training', 'Claude', 'Gemini']
                if not any(kw.lower() in content.lower() for kw in ai_keywords):
                    continue

                # 提取互动数据
                stats = tweet.find('div', class_='tweet-stats')
                retweets = 0
                likes = 0
                if stats:
                    retweet_span = stats.find('span', class_='tweet-stat', string=lambda x: 'retweet' in str(x).lower())
                    like_span = stats.find('span', class_='tweet-stat', string=lambda x: 'like' in str(x).lower())
                    # 简化：暂不解析具体数字

                items.append({
                    'author': account,
                    'content': content[:300],  # 限制长度
                    'url': f"https://twitter.com/{account}",
                    'retweets': retweets,
                    'likes': likes,
                    'source': 'twitter_nitter',
                    'timestamp': datetime.now().isoformat()
                })

        except Exception as e:
            print(f"采集 {account} 失败: {e}")
            continue

    return {
        'success': len(items) > 0,
        'count': len(items),
        'items': items,
        'collected_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    accounts = ['sama', 'ylecun', 'karpathy']
    result = collect_twitter_via_nitter(accounts)
    print(json.dumps(result, ensure_ascii=False, indent=2))
