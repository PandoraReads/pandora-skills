# Apex 习惯打卡小组件

开始前读取根目录 `AGENTS.md`。此仓库把习惯与每日完成记录交给 Apex 的全局习惯小组件，数据保存在 `.obsidian/plugins/apex-dashboard/habits.json`；它们不是 PARA Markdown 数据库。

1. 用户要新增或编辑习惯时，指引其使用 Apex 侧栏中的“习惯打卡”小组件及其中的添加/编辑控件；不要创建 `tracker` 属性、打卡 Markdown 文件、目录或 快速笔记 预设。
2. 用户要回顾时，只有在已连接到仓库且用户请求查看的前提下，读取插件 `habits.json` 中的习惯定义和日期记录。把小组件数据视为唯一来源，不将示范或缺失日期当作真实打卡。
3. 汇总频次、连续天数时以数据记录为准；缺失记录表示未知，不补造、不推断未完成。任何纠错都先保留现有记录并确认依据。
4. 确保 `.obsidian/plugins/apex-dashboard/data.json` 中 `widgetHabitEnabled` 为 `true`。不得改动其他插件配置字段；启用后说明首次建立习惯需在小组件中操作。

## 与 LLM-Wiki 协作

习惯打卡数据仍只在 Apex 小组件；不要把打卡流水复制进 Wiki。回顾习惯方法论时可用 `$pandora-query` 检索 PARA 与 Wiki，但不能用知识卡替代实际记录。
