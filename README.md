# AI内容创作系统 v1.0

## 项目目标

每天自动生成AI前沿资讯情报包和爆款公众号文章。

## 系统架构

```
数据采集层 → 分析处理层 → 内容创作层
  (6源)      (打分+深度)    (选题+成稿)
```

## 执行时间

每天09:10-09:55（45分钟）

## 技术方案

- Twitter: Nitter镜像（免费）
- 融资数据: 爬虫+交叉验证
- 公众号: 自动化浏览器控制（微信读书号）
- GitHub: 对比shkyyy18所有项目（除mi_fitness_data_bridge）
- 风格学习: 花叔+卡兹克+新智元（全学）

## 当前状态

每日直接由 Codex 读取 [AGENTS.md](AGENTS.md) 执行。09:10 启动，09:55 为交付目标。查看 [排程记录](scheduled_task_config.json) 和 [交付状态](STATUS.md)。

## 目录结构

```
intelligence/     # 情报层
  collectors/     # 采集脚本
  analyzers/      # 深度分析
  daily/          # 每日产出
  
creation/         # 创作层
  styles/         # 风格库
  generators/     # 生成器
  drafts/         # 草稿
  
workflows/        # 工作流
  run_all.py      # 采集与初步情报脚本
```

定时交付包含情报、GitHub 分析、选题和审校后的公众号正文。旧脚本的采集结果可作线索，成稿由 Codex 在定时回合中完成。
