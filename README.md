# Pandora Skills

我为知识管理、学习和个人成长创建与改造的 Agent 技能。当前收录十一个 `pandora-*` 技能：八个《潘多拉的数字花园·第二大脑》技能，以及三个学习技能。

第二大脑系列把 **PARA（面向人的原始笔记与行动）** 和 **LLM-Wiki（面向 AI 的可追溯知识层）** 连起来。学习技能用于深度阅读、笔记精华高亮与提问式语言学习。技能文件公开；可直接使用的完整 Obsidian 仓库、笔记模板、工作台配置与示范内容不在此仓库中。

## 技能目录

### 潘多拉的数字花园·第二大脑

| 技能 | 解决的问题 |
| --- | --- |
| [`pandora-onboard`](skills/pandora-onboard/SKILL.md) | 确认并绑定 Obsidian 仓库路径，引导首次使用 |
| [`pandora-triage`](skills/pandora-triage/SKILL.md) | 整理收集箱，按实际用途分流原件 |
| [`pandora-plan`](skills/pandora-plan/SKILL.md) | 规划愿景、领域、年度目标、项目和心愿 |
| [`pandora-ingest`](skills/pandora-ingest/SKILL.md) | 从收集箱或资源摄入可追溯的 LLM-Wiki |
| [`pandora-query`](skills/pandora-query/SKILL.md) | 跨 PARA 与 Wiki 检索，并回到原文核对 |
| [`pandora-lint`](skills/pandora-lint/SKILL.md) | 检查属性、目录、双链及 Wiki 来源链 |
| [`pandora-review`](skills/pandora-review/SKILL.md) | 做周回顾与年度复盘 |
| [`pandora-archive`](skills/pandora-archive/SKILL.md) | 归档或恢复项目与笔记，维护关系和记录 |

### 学习技能

| 技能 | 解决的问题 |
| --- | --- |
| [`pandora-dankoe-reading`](skills/pandora-dankoe-reading/SKILL.md) | 阅读前预分析、阅读后主动回忆、整理见解并追踪应用 |
| [`pandora-hilight`](skills/pandora-hilight/SKILL.md) | 为 Markdown 笔记选取精华、写入 HiLighter 高亮与辅导卡片 |
| [`pandora-socrates-learning`](skills/pandora-socrates-learning/SKILL.md) | 用单步提问、反馈与难度调整练习语言材料 |

## 如何使用

第二大脑系列按《潘多拉的数字花园·第二大脑》的目录、属性和模板约定编写。它们不是一个空仓库生成器；单独下载后，需要先接入满足相应约定的 Obsidian 仓库。依赖与安装步骤见[接入说明](docs/integration.md)。学习技能可单独安装；`pandora-dankoe-reading` 可处理用户提供的阅读材料，`pandora-hilight` 需要 HiLighter 插件及用户指定的 Obsidian 仓库，`pandora-socrates-learning` 可直接使用用户提供的学习材料。

本仓库首页的 [`skills/`](skills/) 直接展示全部技能，[`scripts/`](scripts/) 保存第二大脑路径绑定脚本。接入第二大脑时，将该组八个技能复制到目标 Obsidian 仓库的 `.agents/skills/`，并将绑定脚本复制到 `.agents/scripts/`；先运行 `pandora-onboard`，由它确认实际仓库路径并检查所需结构。复制或搬迁仓库后重新绑定路径。之后可以按名称调用，例如 `$pandora-triage`、`$pandora-query`。学习技能可复制到所用 Agent 工具的技能目录并按各自 `SKILL.md` 使用。

## 关于《潘多拉的数字花园·第二大脑》

这个项目探索如何把 Obsidian 中的收集、规划、项目执行与知识检索组织成一个可长期使用的第二大脑。公开技能展示的是工作方法；完整开箱仓库提供配套目录、笔记模板、Apex 工作台配置和可直接使用的整体结构。项目入口将在发布后补充。

相关开源项目：[Apex Dashboard](https://github.com/PandoraReads/apex-dashboard)（Obsidian 工作台插件）。

## 许可

本仓库代码与技能文本采用 [MIT License](LICENSE)。第三方软件、插件和未收录的完整第二大脑仓库不因此获得授权。
