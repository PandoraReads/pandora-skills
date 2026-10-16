# 接入现有 Obsidian 仓库

本文适用于《潘多拉的数字花园·第二大脑》系列的八个技能。公开仓库提供技能与路径绑定脚本，不包含笔记模板、属性字典、工作台页面或插件配置。使用前请先准备符合以下约定的 Obsidian 仓库，或自行调整技能中的路径与字段。两个学习技能可单独安装；不参与第二大脑路径绑定。

## 必要结构

```text
仓库根目录/
├── AGENTS.md
├── 00 收集箱/
├── 10 项目/
├── 20 领域/
├── 30 资源/
├── 40 归档/
├── 50 日志/
├── 60 工作台/
├── 90 系统/
│   ├── 指南/
│   │   ├── 属性字典.md
│   │   ├── LLM-Wiki协作规范.md
│   │   ├── 日常工作流.md
│   │   └── 年度切换流程.md
│   └── 模板/           # 技能引用的 01–16 号模板
├── wiki/
│   ├── sources/
│   ├── entities/
│   ├── concepts/
│   ├── index.md
│   └── log.md
└── .agents/
    ├── skills/pandora-*/
    └── scripts/bind_vault.py
```

`pandora-onboard` 还会检查 `开始使用-后续改成 html.md`。项目管理与习惯相关流程使用 [Apex Dashboard](https://github.com/PandoraReads/apex-dashboard) 的配置；路径绑定脚本会更新 `.obsidian/plugins/apex-dashboard/data.json` 中的 `skillSourceFolders`。缺少这些配套文件时，请先建立你自己的对应结构，或修改技能与脚本后再执行。

## 安装与绑定

1. 将技能目录中“潘多拉的数字花园·第二大脑”组的八个技能复制到目标仓库的 `.agents/skills/`，将 `scripts/bind_vault.py` 复制到目标仓库的 `.agents/scripts/`。GitHub 仓库本身不需要 `.agents/` 目录。
2. 确认目标仓库确实是你要使用的副本，再运行 `pandora-onboard`。它会要求你提供仓库的绝对路径。
3. 在目标仓库中执行：

   ```bash
   python3 .agents/scripts/bind_vault.py "/你的/Obsidian/仓库绝对路径"
   python3 .agents/scripts/bind_vault.py "/你的/Obsidian/仓库绝对路径" --check
   ```

4. 在支持 Agent 技能的工具中调用 `$pandora-triage`、`$pandora-plan` 等；不支持技能发现时，可以直接读取相应 `SKILL.md`。

绑定脚本要求根目录存在 `AGENTS.md`、`00 收集箱`、`60 工作台`、属性字典和 Apex 配置中的 `skillSourceFolders` 字段。它只更新八个第二大脑技能的仓库路径标记以及该字段；即使同一技能目录中装有学习技能，也不会修改它们。脚本不创建或修改笔记模板。运行前可备份你自己修改过的技能文件和插件设置。

## 数据边界

- PARA 原文与行动是权威来源；Wiki 只保存有来源链的衍生知识。
- `pandora-ingest` 只从 `00 收集箱`、`30 资源` 摄入；其他目录的个人行动不自动变成 Wiki 内容。
- 技能依赖目标仓库的 `AGENTS.md`、属性字典和模板定义。若字段或模板不同，请先对照调整，避免直接写入不兼容的笔记。
- 公开仓库不包含任何用户笔记、私有模板或完整工作台布局。
