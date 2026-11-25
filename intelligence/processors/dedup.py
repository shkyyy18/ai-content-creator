"""去重处理器"""
from difflib import SequenceMatcher

def deduplicate_items(items):
    """去重：标题相似度>80% 或 URL相同

    Args:
        items: 待去重的列表

    Returns:
        去重后的列表
    """
    if not items:
        return []

    unique_items = []
    seen_urls = set()

    for item in items:
        url = item.get('url', '')

        # URL去重
        if url and url in seen_urls:
            continue

        # 标题相似度去重
        is_duplicate = False
        title = item.get('title', '')

        for existing in unique_items:
            existing_title = existing.get('title', '')
            if not title or not existing_title:
                continue

            similarity = SequenceMatcher(None, title, existing_title).ratio()

            if similarity > 0.8:
                # 合并来源
                if 'sources' not in existing:
                    existing['sources'] = [existing.get('source', 'unknown')]
                existing['sources'].append(item.get('source', 'unknown'))

                # 保留更高的热度值
                if item.get('heat_score', 0) > existing.get('heat_score', 0):
                    existing['heat_score'] = item['heat_score']

                is_duplicate = True
                break

        if not is_duplicate:
            item['sources'] = [item.get('source', 'unknown')]
            unique_items.append(item)
            if url:
                seen_urls.add(url)

    return unique_items

def merge_by_category(all_items):
    """按类别合并数据

    Returns:
        {
            'hotspot': [...],
            'product': [...],
            'funding': [...],
            'github': [...],
            'wechat': [...],
            'community': [...]
        }
    """
    categorized = {
        'hotspot': [],
        'product': [],
        'funding': [],
        'github': [],
        'wechat': [],
        'community': []
    }

    for item in all_items:
        source = item.get('source', 'unknown')

        if source in ['weibo', 'twitter']:
            categorized['hotspot'].append(item)
        elif source == 'github':
            categorized['github'].append(item)
        elif source in ['36kr', 'itjuzi']:
            categorized['funding'].append(item)
        elif source == 'wechat':
            categorized['wechat'].append(item)
        elif source in ['hackernews', 'reddit', 'v2ex']:
            categorized['community'].append(item)
        else:
            categorized['product'].append(item)

    return categorized
