"""社区讨论采集器 - HackerNews + Reddit"""
import requests
from datetime import datetime
import json

def collect_hackernews():
    """采集HackerNews首页AI相关话题"""
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    items = []

    try:
        response = requests.get(url, timeout=10)
        story_ids = response.json()[:30]  # 前30条

        ai_keywords = ['AI', 'GPT', 'LLM', 'Claude', 'ChatGPT', 'machine learning', 'neural']

        for story_id in story_ids[:10]:  # 只检查前10条
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=5)
            story = story_response.json()

            title = story.get('title', '')
            if any(kw.lower() in title.lower() for kw in ai_keywords):
                items.append({
                    'title': title,
                    'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'score': story.get('score', 0),
                    'comments': story.get('descendants', 0),
                    'source': 'hackernews',
                    'timestamp': datetime.now().isoformat()
                })

    except Exception as e:
        print(f"HN采集失败: {e}")

    return items

def collect_reddit():
    """采集Reddit r/MachineLearning"""
    url = "https://www.reddit.com/r/MachineLearning/hot.json?limit=10"
    headers = {'User-Agent': 'AI-Content-Creator'}
    items = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        for post in data['data']['children']:
            post_data = post['data']
            items.append({
                'title': post_data['title'],
                'url': f"https://reddit.com{post_data['permalink']}",
                'score': post_data['score'],
                'comments': post_data['num_comments'],
                'source': 'reddit',
                'timestamp': datetime.now().isoformat()
            })

    except Exception as e:
        print(f"Reddit采集失败: {e}")

    return items

def collect_community_data():
    """汇总社区数据"""
    all_items = []

    hn_items = collect_hackernews()
    all_items.extend(hn_items)

    reddit_items = collect_reddit()
    all_items.extend(reddit_items)

    return {
        'success': len(all_items) > 0,
        'count': len(all_items),
        'items': all_items,
        'collected_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    result = collect_community_data()
    print(json.dumps(result, ensure_ascii=False, indent=2))
