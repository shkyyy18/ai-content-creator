"""热度评分器"""
from datetime import datetime
import math

def calculate_heat_score(item):
    """计算热度评分（0-100）

    Args:
        item: 包含source, timestamp, engagement数据的字典
    """
    # 平台权重
    platform_weights = {
        'weibo': 0.30,
        'twitter': 0.25,
        'hackernews': 0.20,
        'github': 0.15,
        'wechat': 0.10,
        '36kr': 0.08,
        'reddit': 0.12
    }

    base_score = platform_weights.get(item.get('source', 'unknown'), 0.05) * 100

    # 互动量评分（对数平滑）- 优化版
    def safe_int(val, default=0):
        try:
            if isinstance(val, str):
                if val == 'unknown':
                    return default
                return int(val.replace(',', ''))
            return int(val) if val else default
        except:
            return default

    # 分平台计算engagement
    source = item.get('source', 'unknown')

    if source == 'weibo':
        # 微博：热度值是关键指标
        engagement = safe_int(item.get('heat', 0)) / 10000  # 35万热度 = 35分
    elif source == 'github_trending':
        # GitHub：stars是关键，今日stars更重要
        stars = safe_int(item.get('stars', 0))
        today_stars = safe_int(item.get('today_stars', 0))
        engagement = stars * 0.5 + today_stars * 5  # 强化今日增长
    elif source == 'hackernews' or source == 'reddit':
        # HN/Reddit：score + 评论数
        engagement = safe_int(item.get('score', 0)) * 3 + safe_int(item.get('comments', 0)) * 2
    else:
        # 其他平台：通用计算
        engagement = (
            safe_int(item.get('likes', 0)) +
            safe_int(item.get('retweets', 0)) * 2 +
            safe_int(item.get('comments', 0)) * 1.5
        )

    if engagement > 0:
        engagement_score = min(math.log10(engagement + 1) * 20, 60)  # 提高上限到60
    else:
        engagement_score = 0

    # 时效加成（新鲜度奖励）
    try:
        timestamp = datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00'))
        hours_ago = (datetime.now(timestamp.tzinfo) - timestamp).total_seconds() / 3600

        # 6小时内给最高分，24小时线性衰减
        if hours_ago < 6:
            time_bonus = 30
        elif hours_ago < 24:
            time_bonus = max(0, 30 - (hours_ago - 6) / 18 * 20)  # 6-24小时衰减到10分
        else:
            time_bonus = max(0, 10 - (hours_ago - 24) / 24 * 10)  # 24-48小时衰减到0
    except:
        time_bonus = 15  # 默认给中等分

    # 综合评分（调整权重）
    total_score = base_score * 0.2 + engagement_score * 0.6 + time_bonus

    return min(total_score, 100)

def classify_by_heat(items):
    """按热度分类

    Returns:
        {
            'explosive': [...],  # >80分
            'hot': [...],        # 50-80分
            'normal': [...]      # <50分
        }
    """
    classified = {
        'explosive': [],
        'hot': [],
        'normal': []
    }

    for item in items:
        score = calculate_heat_score(item)
        item['heat_score'] = score

        if score > 80:
            classified['explosive'].append(item)
        elif score > 50:
            classified['hot'].append(item)
        else:
            classified['normal'].append(item)

    # 排序
    for category in classified:
        classified[category].sort(key=lambda x: x['heat_score'], reverse=True)

    return classified
