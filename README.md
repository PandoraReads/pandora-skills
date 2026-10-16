# Pandora Skills

我为知识管理、学习和个人成长创建与改造的 Agent 技能。当前发布的八个 `pandora-*` 技能，来自《潘多拉的数字花园·第二大脑》的实际工作流。

这组技能把 **PARA（面向人的原始笔记与行动）** 和 **LLM-Wiki（面向 AI 的可追溯知识层）** 连起来。技能文件公开；可直接使用的完整 Obsidian 仓库、笔记模板、工作台配置与示范内容不在此仓库中。

## 技能目录

| 技能 | 解决的问题 |
| --- | --- |
| [`pandora-onboard`](.agents/skills/pandora-onboard/SKILL.md) | 确认并绑定 Obsidian 仓库路径，引导首次使用 |
| [`pandora-triage`](.agents/skills/pandora-triage/SKILL.md) | 整理收集箱，按实际用途分流原件 |
| [`pandora-plan`](.agents/skills/pandora-plan/SKILL.md) | 规划愿景、领域、年度目标、项目和心愿 |
| [`pandora-ingest`](.agents/skills/pandora-ingest/SKILL.md) | 从收集箱或资源摄入可追溯的 LLM-Wiki |
| [`pandora-query`](.agents/skills/pandora-query/SKILL.md) | 跨 PARA 与 Wiki 检索，并回到原文核对 |
| [`pandora-lint`](.agents/skills/pandora-lint/SKILL.md) | 检查属性、目录、双链及 Wiki 来源链 |
| [`pandora-review`](.agents/skills/pandora-review/SKILL.md) | 做周回顾与年度复盘 |
| [`pandora-archive`](.agents/skills/pandora-archive/SKILL.md) | 归档或恢复项目与笔记，维护关系和记录 |

## 如何使用

这些技能按《潘多拉的数字花园·第二大脑》的目录、属性和模板约定编写。它们不是一个空仓库生成器；单独下载后，需要先接入满足相应约定的 Obsidian 仓库。依赖与安装步骤见[接入说明](docs/integration.md)。

将 `.agents/skills/pandora-*` 与 `.agents/scripts/bind_vault.py` 放入目标仓库的相同相对路径后，先运行 `pandora-onboard`，由它确认实际仓库路径并检查所需结构。复制或搬迁仓库后重新绑定路径。之后可以按名称调用，例如 `$pandora-triage`、`$pandora-query`。

## 关于《潘多拉的数字花园·第二大脑》

这个项目探索如何把 Obsidian 中的收集、规划、项目执行与知识检索组织成一个可长期使用的第二大脑。公开技能展示的是工作方法；完整开箱仓库提供配套目录、笔记模板、Apex 工作台配置和可直接使用的整体结构。项目入口将在发布后补充。

相关开源项目：[Apex Dashboard](https://github.com/PandoraReads/apex-dashboard)（Obsidian 工作台插件）。

## 许可

本仓库代码与技能文本采用 [MIT License](LICENSE)。第三方软件、插件和未收录的完整第二大脑仓库不因此获得授权。
