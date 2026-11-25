"""设置定时任务 - 每天09:10自动运行完整流程"""
import os
import sys

print("=" * 60)
print("定时任务配置说明")
print("=" * 60)

task_config = {
    "taskId": "ai-content-daily",
    "title": "AI内容创作日报",
    "description": "每天自动采集AI资讯、生成选题和文章",
    "cronExpression": "10 9 * * *",  # 每天09:10
    "prompt": f"""执行AI内容创作日报任务：

1. 运行完整采集流程
2. 生成情报包
3. 生成选题包
4. GitHub深度分析
5. 生成1篇文章（基于当天最热选题）

工作目录：{os.path.abspath('.')}
执行命令：python workflows/run_all.py
""",
    "notifyOnCompletion": True
}

print(f"\n任务ID：{task_config['taskId']}")
print(f"标题：{task_config['title']}")
print(f"执行时间：每天09:10")
print(f"工作目录：{task_config['prompt'].split('工作目录：')[1].split('执行命令')[0].strip()}")

print("\n" + "=" * 60)
print("定时任务已配置（待接入Codex）")
print("=" * 60)

# 保存配置供后续使用
import json
with open('scheduled_task_config.json', 'w', encoding='utf-8') as f:
    json.dump(task_config, f, ensure_ascii=False, indent=2)

print("\n✓ 配置已保存到 scheduled_task_config.json")
print("\n下一步：将此任务接入 D:/AgentHub/tasks/")
