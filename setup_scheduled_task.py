"""读取本地排程记录。任务由 Codex 创建并执行。"""

import json
from pathlib import Path


if __name__ == "__main__":
    record = Path(__file__).with_name("scheduled_task_config.json")
    task = json.loads(record.read_text(encoding="utf-8"))
    print(f"{task['title']}（{task['taskId']}）")
    print(f"时区与执行时间：{task['timezone']} {task['schedule']}")
    print(f"执行规则：{task['runbook']}")
    print("当前启停状态在 Codex 定时任务列表查看。")
