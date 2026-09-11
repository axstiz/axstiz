#!/usr/bin/env python3
"""Сгенерировать резюме.md из site/data.json.

Usage:
    python tools/resume_gen.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "site" / "data.json"
OUT_PATH = ROOT / "резюме.md"


def social(data: dict, label: str) -> dict:
    wanted = label.lower()
    for s in data.get("socials", []):
        if s.get("label", "").lower() == wanted:
            return s
    return {}


def build(data: dict) -> str:
    profile = data.get("profile", {})
    resume = data.get("resume", {})
    lines: list[str] = []

    def blank() -> None:
        lines.append("")

    # ---- шапка ----
    lines.append(f"# {profile.get('fullName', profile.get('name', ''))}  ")
    blank()
    lines.append(f"📍Город: {profile.get('location', '')}  ")
    blank()
    lines.append(f"Номер телефона: {profile.get('phone', '')}  ")
    blank()
    email = social(data, "email").get("handle", "")
    lines.append(f"Почта: {email}  ")
    blank()
    tg = social(data, "telegram").get("handle", "")
    lines.append(f"Tg: {tg}  ")
    blank()

    gh = social(data, "github").get("url", "")
    gv = social(data, "gitverse").get("url", "")
    lc = resume.get("leetcode", {})
    links = f"🔗 [GitHub]({gh}) 🔗 [Gitverse]({gv}) 🔗 [LeetCode]({lc.get('url', '')})"
    if lc.get("solved"):
        links += (
            f" ({lc['solved']} задач: {lc.get('medium', 0)} medium, "
            f"{lc.get('hard', 0)} hard)"
        )
    lines.append(links)
    blank()

    objective = resume.get("objective", "")
    lines.append(f"##### > {objective}")
    blank()

    # ---- опыт работы ----
    lines.append("---")
    blank()
    lines.append("## > Опыт работы")
    blank()
    for exp in resume.get("experience", []):
        proj = exp.get("project", {})
        lines.append(f"##### {exp.get('title', '')}")
        lines.append(f"[{proj.get('name', '')}]({proj.get('url', '')}) — {exp.get('context', '')}")
        blank()
        roles = ", ".join(f"`{r}`" for r in exp.get("role", []))
        lines.append(f"Роль: {roles}")
        blank()
        lines.append(exp.get("summary", ""))
        blank()
        lines.append("**Ключевые результаты и архитектурные решения:**")
        blank()
        for bullet in exp.get("results", []):
            lines.append(f"- {bullet}")
        blank()
        if exp.get("metrics"):
            lines.append(exp["metrics"])
            blank()
        if exp.get("pipeline"):
            lines.append(exp["pipeline"])
            blank()
    lines.append("---")
    blank()

    # ---- образование ----
    higher = [e for e in data.get("education", []) if e.get("type") != "additional"]
    lines.append("## > Образование")
    blank()
    for edu in higher:
        lines.append(f"##### **{edu.get('institution', '')}**")
        note = f" ({edu.get('periodNote', '')})" if edu.get("periodNote") else ""
        lines.append(f"> *{edu.get('period', '')}{note}*")
        blank()
        lines.append(f"Институт: **{edu.get('institute', '')}**")
        lines.append(f"- Образовательная программа: «{edu.get('program', '')}»")
        disciplines = edu.get("disciplines", [])
        if disciplines:
            lines.append(f"- Ключевые дисциплины: {', '.join(disciplines)}")
        blank()
    lines.append("---")
    blank()

    # ---- дополнительное образование ----
    additional = [e for e in data.get("education", []) if e.get("type") == "additional"]
    if additional:
        lines.append("## > Дополнительное образование")
        blank()
        for edu in additional:
            title = edu.get("institution", "")
            program = edu.get("program", "")
            lines.append(f"##### {title} | {program}" if program else f"##### {title}")
            status = f" ({edu.get('status', '')})" if edu.get("status") else ""
            lines.append(f"> *{edu.get('period', '')}*{status}")
            blank()
        lines.append("---")
        blank()

    # ---- технические навыки ----
    lines.append("## > Технические навыки")
    blank()
    lines.append("| Категория | Навыки |")
    lines.append("| --------- | ------ |")
    for group in data.get("stack", []):
        items = ", ".join(group.get("items", []))
        lines.append(f"| **{group.get('category', '')}** | {items} |")
    blank()

    # ---- ключевые компетенции ----
    lines.append("## > Ключевые компетенции")
    blank()
    for c in resume.get("competencies", []):
        lines.append(f"- {c}")
    blank()
    lines.append("---")
    blank()

    # ---- личные качества ----
    lines.append("## > Личные качества")
    blank()
    for q in resume.get("personalQualities", []):
        text = q.get("text", "")
        line = f"- **{q.get('name', '')}**"
        if text:
            line += f": {text}"
        lines.append(line)
    blank()

    return "\n".join(lines) + "\n"


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    OUT_PATH.write_text(build(data), encoding="utf-8", newline="\n")
    print(f"OK: {OUT_PATH}")


if __name__ == "__main__":
    main()