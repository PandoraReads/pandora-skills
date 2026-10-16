#!/usr/bin/env python3
"""Bind packaged Pandora skill instructions to a confirmed Obsidian vault path."""

import argparse
import json
import pathlib
import re
import sys


MARKER = "仓库根路径（由 pandora-onboard 确认并更新）："
REQUIRED = ("AGENTS.md", "00 收集箱", "60 工作台", "90 系统/指南/属性字典.md")
SECOND_BRAIN_SKILLS = (
    "pandora-onboard", "pandora-triage", "pandora-plan", "pandora-ingest",
    "pandora-query", "pandora-lint", "pandora-review", "pandora-archive",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="将当前仓库绝对路径同步到 Pandora 技能")
    parser.add_argument("vault", help="用户确认的 Obsidian 仓库绝对路径")
    parser.add_argument("--check", action="store_true", help="只检查绑定，不写入")
    args = parser.parse_args()
    supplied = pathlib.Path(args.vault).expanduser()
    if not supplied.is_absolute():
        print("请提供用户确认的绝对路径", file=sys.stderr)
        return 1
    vault = supplied.resolve()
    if not all((vault / item).exists() for item in REQUIRED):
        print("不是有效的 Pandora 仓库根目录：缺少 AGENTS.md、00 收集箱、60 工作台或属性字典", file=sys.stderr)
        return 1
    skills = [vault / ".agents/skills" / name / "SKILL.md" for name in SECOND_BRAIN_SKILLS]
    missing = [skill for skill in skills if not skill.is_file()]
    if missing:
        print(f"缺少第二大脑技能：{', '.join(str(skill) for skill in missing)}", file=sys.stderr)
        return 1
    config_path = vault / ".obsidian/plugins/apex-dashboard/data.json"
    try:
        config_text = config_path.read_text(encoding="utf-8")
        config = json.loads(config_text)
    except (OSError, json.JSONDecodeError) as error:
        print(f"无法读取 Apex 设置：{error}", file=sys.stderr)
        return 1
    if not isinstance(config, dict) or "skillSourceFolders" not in config:
        print("Apex 设置缺少 skillSourceFolders", file=sys.stderr)
        return 1
    expected_folder = str(vault / ".agents/skills")
    config_stale = config["skillSourceFolders"] != expected_folder
    updated_config, replacement_count = re.subn(
        r'("skillSourceFolders"\s*:\s*)"(?:\\.|[^"\\])*"',
        lambda match: match.group(1) + json.dumps(expected_folder, ensure_ascii=False),
        config_text,
        count=1,
    )
    if replacement_count != 1:
        print("无法在 Apex 设置中定位技能文件夹字段", file=sys.stderr)
        return 1
    stale = []
    updates = []
    for skill in skills:
        body = skill.read_text(encoding="utf-8")
        lines = body.splitlines(keepends=True)
        matches = [i for i, line in enumerate(lines) if line.startswith(MARKER)]
        if len(matches) != 1:
            print(f"路径标记缺失或重复：{skill}", file=sys.stderr)
            return 1
        index = matches[0]
        expected = f"{MARKER}`{vault}`\n"
        if lines[index] != expected:
            stale.append(skill)
            lines[index] = expected
            updates.append((skill, "".join(lines)))
    if args.check and (stale or config_stale):
        print("技能路径或 Apex 技能文件夹尚未绑定到当前仓库", file=sys.stderr)
        return 1
    if not args.check:
        for skill, body in updates:
            skill.write_text(body, encoding="utf-8")
        if config_stale:
            config_path.write_text(updated_config, encoding="utf-8")
    print(f"已核对 {len(skills)} 个技能及 Apex 技能文件夹；仓库根路径：{vault}；更新 {0 if args.check else len(stale)} 个技能")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
