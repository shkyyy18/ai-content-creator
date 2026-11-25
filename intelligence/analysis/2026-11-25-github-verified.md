# GitHub 分析｜2026 年 11 月 25 日

本地研究使用当日 Trending 和 GitHub API。按项目规则排除 Mi Fitness Data Bridge 后，账号接口返回 13 个自有仓库，其中 3 个公开、10 个私有。公开仓库核到了 README，私有仓库只核对账号可见的元数据。以下使用公开资料做具体对照。

## Trending 口径

| 项目 | Trending 当日新增 | API 累计星标 | 可借鉴的设计 |
| --- | ---: | ---: | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | 1,003 | 325,920 | README 按 Codex App、Codex CLI 等入口组织安装，并把验证步骤写进执行计划。 |
| [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | 1,074 | 64,957 | 工具目录展示入口，Skill 和 CLI 承接执行，便于使用者找到能跑的第一个动作。 |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 802 | 72,213 | README 在安装之前或附近展示图样与用途，让使用者先判断交付是否符合需求。 |

星标为本次抓取快照。初稿将页面标注的 `stars today` 当成累计星标，再和账号仓库取平均，统计口径不一致。来源为 [Trending](https://github.com/trending) 和 [Superpowers API](https://api.github.com/repos/obra/superpowers)、[CLI-Anything API](https://api.github.com/repos/HKUDS/CLI-Anything)、[diagram-design API](https://api.github.com/repos/cathrynlavery/diagram-design)。

## 和现有项目的差别

| 现有公开仓库 | 已有能力 | 值得验证的改动 |
| --- | --- | --- |
| [AI 商业顾问](https://github.com/shkyyy18/ai-business-growth-validation-agent) | README 有交付场景表、首次使用、离线检查和空白模板。 | 选择一个合成委托，在 README 首屏串起输入、离线执行、交付表和复核动作。按 Superpowers 的思路，让新用户能按步骤看到一份完整结果。 |
| [健康顾问公开版](https://github.com/shkyyy18/health-advisor-internal) | 已有演示素材、适配范围及本地安装路径。 | 参考 diagram-design，把最能说明用途的图和启动步骤相邻摆放。用合成数据展示从记录到看板的结果，并标出使用场景。 |
| [微存 WeSave](https://github.com/shkyyy18/wechat-video-skills) | README 已有按系统选包、自然语言入口、质量检查与真机待验说明。 | 参考 CLI-Anything 的入口组织，把安装后的第一个动作与退出状态放在一起。优先核对首次使用者能否分清获取原文件和录制副本。 |

首选本地验证项是商业顾问的合成委托示例。检查一个首次打开项目的人能否凭 README 找到输入、得到输出、复核交付。私有项目的入口、文档和实际运行情况本轮无正文证据，保留为待核。
