"""选题生成器 - 从情报包提炼可执行选题"""
from datetime import datetime

def generate_topics(items, top_n=5):
    """从采集的信息生成选题

    Args:
        items: 情报列表
        top_n: 生成选题数量

    Returns:
        选题列表，每个选题包含：标题、角度、目标受众、论点、素材
    """

    topics = []

    # 按热度排序
    sorted_items = sorted(items, key=lambda x: x.get('heat_score', 0), reverse=True)

    # 选题模板
    templates = [
        {
            'type': '技术解读',
            'angle': '技术原理与创新点解析',
            'audience': 'AI开发者、技术爱好者'
        },
        {
            'type': '行业观察',
            'angle': '趋势分析与影响预测',
            'audience': 'AI从业者、创业者'
        },
        {
            'type': '实战案例',
            'angle': '落地应用与变现方法',
            'audience': '内容创作者、副业人群'
        },
        {
            'type': '深度对比',
            'angle': '多个相关事件的对比分析',
            'audience': '决策者、研究人员'
        },
        {
            'type': '快讯聚合',
            'angle': '本周AI大事件盘点',
            'audience': '泛AI兴趣人群'
        }
    ]

    # 策略1：单一热点深度解读（前2个）
    for i in range(min(2, len(sorted_items))):
        item = sorted_items[i]
        title = item.get('title', item.get('name', ''))

        topic = {
            'id': i + 1,
            'title': f"深度｜{title}：技术突破还是营销噱头？",
            'angle': '技术原理、应用场景、局限性三维分析',
            'audience': 'AI开发者、技术管理者',
            'thesis': f"解析{title}的核心创新，评估其实际价值与商业前景",
            'materials': [
                {'source': item.get('source'), 'url': item.get('url'), 'type': '主素材'},
                {'source': 'GitHub', 'url': '', 'type': '相关开源项目'},
                {'source': '技术论坛', 'url': '', 'type': '社区讨论'}
            ],
            'structure': [
                '1. 技术背景（200字）',
                '2. 核心创新点（400字）',
                '3. 应用场景与局限（400字）',
                '4. 商业前景与启示（300字）',
                '5. 对个人开发者的建议（200字）'
            ],
            'estimated_length': 1500,
            'estimated_time': '2-3小时'
        }
        topics.append(topic)

    # 策略2：多个热点聚合（1个）
    if len(sorted_items) >= 3:
        aggregated_items = sorted_items[:5]
        topic = {
            'id': 3,
            'title': f"本周AI大事件｜{len(aggregated_items)}个不容错过的技术进展",
            'angle': '快讯聚合+趋势洞察',
            'audience': 'AI从业者、关注前沿的决策者',
            'thesis': '本周AI领域的关键进展与趋势信号',
            'materials': [
                {'source': item.get('source'), 'url': item.get('url'), 'title': item.get('title', item.get('name'))}
                for item in aggregated_items
            ],
            'structure': [
                '1. 本周最重要的突破（300字）',
                f"2. {len(aggregated_items)}个关键事件速览（每个150字）",
                '3. 趋势洞察：这些事件透露了什么信号？（400字）',
                '4. 给创作者的机会（200字）'
            ],
            'estimated_length': 1500,
            'estimated_time': '1.5-2小时'
        }
        topics.append(topic)

    # 策略3：实战应用（1个）- 聚焦变现和落地
    practical_items = [item for item in sorted_items if '变现' in item.get('title', '') or 'GPT' in item.get('title', '')]
    if len(practical_items) > 0:
        item = practical_items[0]
        topic = {
            'id': 4,
            'title': "普通人如何用AI月入过万？3个被验证的变现路径",
            'angle': '实战方法论+案例拆解',
            'audience': '内容创作者、副业人群、自由职业者',
            'thesis': 'AI不是威胁，而是放大器——找到你的AI变现公式',
            'materials': [
                {'source': item.get('source'), 'url': item.get('url'), 'type': '案例素材'},
                {'source': '自有经验', 'url': '', 'type': 'AI写作、图像生成实战'},
                {'source': '社群调研', 'url': '', 'type': '真实变现数据'}
            ],
            'structure': [
                '1. 引子：AI变现不是骗局（200字）',
                '2. 路径1：AI内容创作（400字）',
                '3. 路径2：AI工具代理（400字）',
                '4. 路径3：AI咨询服务（400字）',
                '5. 避坑指南与行动清单（200字）'
            ],
            'estimated_length': 1600,
            'estimated_time': '2-3小时'
        }
        topics.append(topic)

    # 策略4：争议话题（1个）
    controversial_items = [item for item in sorted_items if '马斯克' in item.get('title', '') or '换脸' in item.get('title', '')]
    if len(controversial_items) > 0:
        item = controversial_items[0]
        topic = {
            'id': 5,
            'title': "AI真假难辨时代，我们该如何保持清醒？",
            'angle': '伦理思考+技术科普',
            'audience': '泛人群、关注AI伦理的读者',
            'thesis': 'AI技术快速发展背后的信任危机与应对之道',
            'materials': [
                {'source': item.get('source'), 'url': item.get('url'), 'type': '热点事件'},
                {'source': '技术解析', 'url': '', 'type': 'AI检测技术现状'},
                {'source': '法律法规', 'url': '', 'type': '相关政策与规范'}
            ],
            'structure': [
                '1. 热点事件回顾（200字）',
                '2. AI造假的技术门槛有多低？（400字）',
                '3. 普通人如何辨别真假？（400字）',
                '4. 未来：技术监管与个人防护（300字）',
                '5. 结语：拥抱AI但保持警惕（200字）'
            ],
            'estimated_length': 1500,
            'estimated_time': '2-3小时'
        }
        topics.append(topic)

    return topics[:top_n]


if __name__ == '__main__':
    # 测试
    test_items = [
        {'title': 'GPT-6发布', 'heat_score': 85, 'source': 'hackernews', 'url': 'https://...'},
        {'title': '05后用AI日入4千', 'heat_score': 72, 'source': 'weibo', 'url': 'https://...'},
        {'title': '马斯克说视频不是AI', 'heat_score': 68, 'source': 'weibo', 'url': 'https://...'},
    ]

    topics = generate_topics(test_items)
    for topic in topics:
        print(f"\n选题{topic['id']}：{topic['title']}")
        print(f"受众：{topic['audience']}")
        print(f"预计字数：{topic['estimated_length']} | 预计耗时：{topic['estimated_time']}")
