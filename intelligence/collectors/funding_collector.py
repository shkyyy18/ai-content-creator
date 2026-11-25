"""投融资数据采集器（36氪+IT桔子爬虫）"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

def collect_funding_36kr():
    """采集36氪融资快讯"""
    url = "https://36kr.com/newsflashes"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    items = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找融资相关快讯
        articles = soup.find_all('div', class_='item-title')[:20]

        for article in articles:
            title = article.get_text(strip=True)

            # 过滤融资关键词
            funding_keywords = ['融资', '投资', '获得', '完成', '轮', '美元', '人民币', '估值']
            if not any(kw in title for kw in funding_keywords):
                continue

            # 提取金额（简化版，实际需要更复杂的正则）
            amount_match = re.search(r'(\d+\.?\d*)(亿|万|百万|千万)(美元|人民币|元)', title)
            amount = amount_match.group(0) if amount_match else 'unknown'

            # 提取轮次
            round_match = re.search(r'(天使|A|B|C|D|E|F|Pre-A|Pre-B)\+?轮', title)
            round_type = round_match.group(0) if round_match else 'unknown'

            items.append({
                'title': title,
                'amount': amount,
                'round': round_type,
                'source': '36kr',
                'url': url,
                'timestamp': datetime.now().isoformat()
            })

    except Exception as e:
        print(f"36氪采集失败: {e}")

    return items

def collect_funding_itjuzi():
    """采集IT桔子融资事件"""
    # IT桔子需要登录，这里仅作占位
    return []

def collect_funding_data():
    """汇总融资数据"""
    all_items = []

    # 36氪
    kr_items = collect_funding_36kr()
    all_items.extend(kr_items)

    # IT桔子（待实现）
    # itjuzi_items = collect_funding_itjuzi()
    # all_items.extend(itjuzi_items)

    # 过滤：金额≥100万美元
    # （简化版，实际需要转换人民币）

    return {
        'success': len(all_items) > 0,
        'count': len(all_items),
        'items': all_items,
        'collected_at': datetime.now().isoformat()
    }

if __name__ == '__main__':
    result = collect_funding_data()
    print(json.dumps(result, ensure_ascii=False, indent=2))
