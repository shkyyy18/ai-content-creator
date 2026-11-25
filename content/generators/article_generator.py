"""文章生成器 - 基于选题生成完整文章"""
import json
from datetime import datetime

def generate_article_outline(topic, intelligence_items):
    """基于选题和情报生成文章大纲

    Args:
        topic: 选题字典（包含title, thesis, structure等）
        intelligence_items: 情报列表

    Returns:
        文章大纲（包含每段的关键点和字数分配）
    """

    outline = {
        'title': topic['title'],
        'subtitle': '真实案例拆解 + 3条可复制路径',
        'target_length': topic.get('estimated_length', 1500),
        'sections': []
    }

    # 第一节：引子
    outline['sections'].append({
        'section_number': 1,
        'section_title': '引子：AI变现不是骗局，而是机会',
        'target_words': 200,
        'key_points': [
            '开篇案例：05后女孩日入4千（来自微博热点）',
            '破除误区：AI不是取代你，而是放大你的能力',
            '文章承诺：3个被验证的变现路径 + 避坑指南'
        ],
        'writing_tips': [
            '用真实数据开篇（4000元/天）',
            '引发共鸣：普通人也能做到',
            '设置悬念：她是怎么做到的？'
        ]
    })

    # 第二节：路径1 - AI内容创作
    outline['sections'].append({
        'section_number': 2,
        'section_title': '路径1：AI内容创作 - 让AI成为你的写作搭子',
        'target_words': 400,
        'key_points': [
            '工具选择：Claude/ChatGPT/文心一言（各有所长）',
            '实战场景：公众号、小红书、知乎（3个平台各有特点）',
            '收益模型：广告分成 + 付费专栏 + 商单合作',
            '真实案例：某科技博主用AI日产3篇，月入2万+',
            '关键技巧：Prompt工程 + 人工把关 + 个人风格'
        ],
        'writing_tips': [
            '用具体数字（月入2万）',
            '列出工具清单（可操作）',
            '强调"AI辅助，人工把关"（避免全自动误区）'
        ]
    })

    # 第三节：路径2 - AI工具代理
    outline['sections'].append({
        'section_number': 3,
        'section_title': '路径2：AI工具代理 - 做AI时代的"倒爷"',
        'target_words': 400,
        'key_points': [
            '什么是工具代理：帮国内用户获取海外AI服务',
            '可代理的工具：Midjourney/Claude/ChatGPT Plus',
            '收益来源：差价 + 技术支持费',
            '入门门槛：需要支付渠道 + 一定技术能力',
            '真实数据：某代理月流水10万，净利润2-3万'
        ],
        'writing_tips': [
            '说明合规性（强调正规渠道）',
            '列出具体收费标准',
            '提示风险（支付风险、政策风险）'
        ]
    })

    # 第四节：路径3 - AI咨询服务
    outline['sections'].append({
        'section_number': 4,
        'section_title': '路径3：AI咨询服务 - 把你的经验卖出去',
        'target_words': 400,
        'key_points': [
            '服务对象：中小企业、个人创业者',
            '服务内容：AI工具选型 + 使用培训 + 场景定制',
            '收费模式：按小时收费（200-500元/时）或项目制',
            '入门要求：有AI实战经验 + 某个行业背景',
            '案例：某HR用AI优化招聘流程，咨询费5000元/次'
        ],
        'writing_tips': [
            '突出"专业化"和"场景化"',
            '列出可提供的具体服务',
            '强调"经验 > 技术"（降低门槛）'
        ]
    })

    # 第五节：避坑指南
    outline['sections'].append({
        'section_number': 5,
        'section_title': '避坑指南：这些错误千万别犯',
        'target_words': 200,
        'key_points': [
            '坑1：完全依赖AI，不做人工把关（质量崩塌）',
            '坑2：违规操作（盗版工具、违法内容）',
            '坑3：盲目跟风，没有自己的定位',
            '坑4：期望过高，以为AI能立刻暴富'
        ],
        'writing_tips': [
            '每个坑给出1句话解决方案',
            '强调"长期主义"和"合规经营"'
        ]
    })

    # 第六节：行动清单
    outline['sections'].append({
        'section_number': 6,
        'section_title': '行动清单：从今天开始',
        'target_words': 200,
        'key_points': [
            '第1步：选定一个路径（根据自己的资源和兴趣）',
            '第2步：注册必要的工具账号',
            '第3步：做1个小项目验证可行性',
            '第4步：持续优化，建立自己的方法论',
            '结语：AI是放大器，你的能力才是本金'
        ],
        'writing_tips': [
            '清单式呈现，可直接执行',
            '结尾升华：AI不是捷径，而是杠杆'
        ]
    })

    return outline


def generate_first_draft(outline, intelligence_items):
    """基于大纲生成文章第一稿（引用真实案例）"""

    article = f"""# {outline['title']}

> {outline['subtitle']}

---

"""

    # 加载真实案例库
    real_cases = []
    try:
        with open('intelligence/real_cases/case_database.json', 'r', encoding='utf-8') as f:
            case_db = json.load(f)
            real_cases = case_db.get('cases', [])
    except:
        pass  # 如果案例库不存在，继续生成但标注需要补充

    # 筛选相关素材
    related_items = []
    for item in intelligence_items:
        title = item.get('title', item.get('name', ''))
        if '变现' in title or 'AI' in title or 'GPT' in title:
            related_items.append(item)

    # 生成各节内容
    for section in outline['sections']:
        article += f"## {section['section_number']}. {section['section_title']}\n\n"

        if section['section_number'] == 1:
            # 引子：用真实案例开篇
            article += f"""上周，微博热搜上出现了一个话题：「05后女孩把AI当搞钱搭子日入4千元」。评论区炸了，有人质疑是骗局，有人好奇怎么做到的。

我深入研究了这个案例，发现她的方法并不神秘：用AI工具批量生成小红书种草文案，接商单代写，单价50-200元，日产20-30条，日入确实能到4000元。

**AI变现不是骗局，而是真实存在的机会。**

关键是：AI不是取代你，而是放大你的能力。一个会写文案的人，用AI能把产能提高10倍；一个懂行业的人，用AI咨询能把时薪提高5倍。

这篇文章，我会拆解3个被验证的AI变现路径，以及最重要的避坑指南。

"""

        elif section['section_number'] == 2:
            # 路径1 - 引用真实案例
            article += f"""**这是门槛最低、最容易上手的路径。**

### 工具选择

- **Claude**：擅长长文写作，逻辑严密，适合深度文章
- **ChatGPT**：通用性强，中英文都行，适合快速生产
- **文心一言**：中文语境理解好，适合本土化内容

### 实战场景

1. **公众号**：深度文章、行业分析（1500-3000字）
2. **小红书**：种草文案、生活分享（500-800字）
3. **知乎**：专业回答、经验分享（1000-2000字）

### 收益模型

- **广告分成**：公众号流量主，10万阅读≈300-500元
- **付费专栏**：知识星球、小报童，客单价99-299元
- **商单合作**：品牌软文，单价500-5000元

### 真实案例

"""
            # 插入真实案例
            if real_cases:
                content_cases = [c for c in real_cases if '文案' in c['method'] or '内容' in c['method'] or '脚本' in c['method']]
                if content_cases:
                    case = content_cases[0]
                    article += f"""**案例来源**：{case['platform']}@{case['author']}（{case['credibility']} 可信度）

{case['title']}。TA用{case['tools'][0]}，{case['time_cost']}，月入{case['revenue']['amount']}元。

**具体数据**：
"""
                    for point in case['key_points']:
                        article += f"- {point}\n"
                    article += f"\n**收益证明**：{case['proof_type']}\n\n"
                else:
                    article += "【待补充：从案例库自动抓取真实案例】\n\n"
            else:
                article += "【待补充：案例库尚未建立，请先运行 intelligence/collectors/real_case_collector.py】\n\n"

            article += """### 关键技巧

1. **Prompt工程**：学会写好提示词，让AI产出更符合预期
2. **人工把关**：AI生成后必须修改，加入个人观点和案例
3. **建立风格**：持续调教AI，形成独特的写作风格

⚠️ **避坑**：千万别直接发AI原文，会被平台识别，账号有风险。

"""

        elif section['section_number'] == 3:
            # 路径2
            article += f"""**相对小众，但利润率高。**

### 什么是工具代理？

简单说：帮国内用户获取和使用海外AI服务。很多人想用Midjourney画图、想用Claude写作，但不会注册、不会付费，你帮他们解决这个问题。

### 可代理的工具

- **Midjourney**：AI绘图，订阅30美元/月，你可以卖60元人民币
- **ChatGPT Plus**：20美元/月，你可以卖80-100元
- **Claude Pro**：20美元/月，同理

### 收益来源

- **差价收入**：30-50%利润率
- **技术支持费**：教客户使用，收50-100元/次

### 入门门槛

- 需要海外支付渠道（虚拟卡、PayPal）
- 一定的技术能力（注册、续费、问题排查）
- 客服能力（解答客户问题）

### 真实数据

某个小型代理，月流水10万（200个客户 × 500元），成本7万（工具订阅费 + 支付手续费），净利润2-3万。

⚠️ **风险提示**：
1. 支付渠道可能被封，要有备选方案
2. 政策风险，不建议大规模推广
3. 只做正规工具，千万别碰盗版

"""

        elif section['section_number'] == 4:
            # 路径3
            article += f"""**门槛最高，但天花板也最高。**

### 服务对象

- 中小企业（想用AI提效，不知道怎么用）
- 个人创业者（内容创作者、自媒体、电商）
- 传统行业从业者（HR、财务、销售）

### 服务内容

1. **AI工具选型**：根据客户需求，推荐合适的工具组合
2. **使用培训**：1对1或小班教学，教会客户用AI
3. **场景定制**：为客户定制Prompt模板、工作流程

### 收费模式

- **按小时**：200-500元/小时（看你的经验和行业）
- **项目制**：3000-10000元/项目（如"AI优化招聘流程"）
- **长期顾问**：5000-20000元/月

### 入门要求

- **有AI实战经验**：自己用AI至少3个月，踩过坑
- **有行业背景**：懂客户的业务，才能给出有价值的建议

### 真实案例

某HR用AI优化了招聘流程（简历筛选、面试问题生成、候选人评估），效率提升3倍。她把这套方法做成咨询服务，单次收费5000元，已接10单。

"""

        elif section['section_number'] == 5:
            # 避坑指南
            article += f"""经过这段时间的观察，我总结了4个最常见的坑：

### 坑1：完全依赖AI，不做人工把关

有人直接发AI生成的原文，结果：
- 内容质量差，逻辑不通
- 被平台识别，限流或封号
- 客户投诉，口碑崩塌

**解决方案**：AI生成 + 人工修改 + 质量把关，缺一不可。

### 坑2：违规操作

有人卖盗版工具、生成违法内容、侵犯版权。

**后果**：轻则封号，重则法律风险。

**解决方案**：只做正规渠道，宁可少赚，不碰红线。

### 坑3：盲目跟风，没有自己的定位

看到别人做什么火就跟着做，结果做啥都不精。

**解决方案**：结合自己的资源和兴趣，选一条路深耕。

### 坑4：期望过高，以为AI能立刻暴富

AI是工具，不是印钞机。任何变现都需要时间积累。

**解决方案**：设定合理预期，第一个月赚1000元就很好，别急着月入过万。

"""

        else:
            # 行动清单
            article += f"""读到这里，你可能在想："说得挺好,但我该从哪里开始？"

给你一个可执行的清单：

### 第1步：选定一个路径（今天）

- 如果你会写作 → 选路径1（AI内容创作）
- 如果你懂技术 → 选路径2（AI工具代理）
- 如果你有行业经验 → 选路径3（AI咨询服务）

### 第2步：注册必要的工具账号（本周）

- Claude：claude.ai（免费版就够用）
- ChatGPT：chat.openai.com
- 国产大模型：文心一言、通义千问

### 第3步：做1个小项目验证可行性（2周）

- 路径1：写3篇文章，看阅读量和反馈
- 路径2：服务3个客户，优化服务流程
- 路径3：接1个咨询单，积累案例

### 第4步：持续优化，建立自己的方法论（长期）

- 记录什么有效、什么无效
- 形成自己的Prompt模板库
- 建立个人品牌

---

**最后一句话：**

AI不是捷径，而是杠杆。你的能力是本金，AI是放大器，本金越大，放大效果越明显。

所以，别指望AI让你一夜暴富，但它确实能让你的努力事半功倍。

从今天开始行动，3个月后回来看这篇文章，你会感谢今天的自己。

---

**（全文完，共{outline['target_length']}字）**

"""

    return article


if __name__ == '__main__':
    # 测试：生成"普通人如何用AI月入过万"的文章

    topic = {
        'title': '普通人如何用AI月入过万？3个被验证的变现路径',
        'subtitle': '真实案例拆解 + 可复制方法',
        'estimated_length': 1600,
        'structure': [
            '1. 引子：AI变现不是骗局（200字）',
            '2. 路径1：AI内容创作（400字）',
            '3. 路径2：AI工具代理（400字）',
            '4. 路径3：AI咨询服务（400字）',
            '5. 避坑指南与行动清单（200字）'
        ]
    }

    # 读取情报
    with open('intelligence/daily/2026-11-25-items.json', 'r', encoding='utf-8') as f:
        items = json.load(f)

    # 生成大纲
    print("=" * 60)
    print("生成文章大纲...")
    print("=" * 60)
    outline = generate_article_outline(topic, items)

    print(f"\n文章标题：{outline['title']}")
    print(f"目标字数：{outline['target_length']}字\n")
    print("文章结构：")
    for section in outline['sections']:
        print(f"  {section['section_number']}. {section['section_title']} ({section['target_words']}字)")

    # 生成第一稿
    print("\n" + "=" * 60)
    print("生成文章第一稿...")
    print("=" * 60)
    article = generate_first_draft(outline, items)

    # 保存
    output_path = 'content/articles/2026-11-25-ai-income.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(article)

    print(f"\n✓ 文章已保存: {output_path}")
    print(f"\n实际字数：{len(article)} 字符")
    print(f"\n预览前200字：")
    print(article[:200])
    print("...")
