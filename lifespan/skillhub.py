#!/usr/bin/env python3
"""
SkillHub - AI Agent Skills Marketplace Client
Browse, search, download, and install skills from SkillsMP for OpenCode and other AI agents.
"""

import os
import sys
import json
import shutil
import textwrap
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

import requests
from rich import box
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich.live import Live

console = Console()

API_BASE = "https://www.agentskills.in/api"

AGENTS = {
    "opencode": {
        "name": "OpenCode",
        "global_dir": "~/.config/opencode/skills",
        "local_dir": ".opencode/skills",
    },
    "claude": {
        "name": "Claude Code",
        "global_dir": "~/.claude/skills",
        "local_dir": ".claude/skills",
    },
    "cursor": {
        "name": "Cursor",
        "global_dir": "~/.cursor/skills",
        "local_dir": ".cursor/skills",
    },
    "copilot": {
        "name": "GitHub Copilot",
        "global_dir": "~/.github/skills",
        "local_dir": ".github/skills",
    },
    "codex": {
        "name": "OpenAI Codex",
        "global_dir": "~/.codex/skills",
        "local_dir": ".codex/skills",
    },
    "windsurf": {
        "name": "Windsurf",
        "global_dir": "~/.codeium/windsurf/skills",
        "local_dir": ".windsurf/skills",
    },
    "cline": {
        "name": "Cline",
        "global_dir": "~/.cline/skills",
        "local_dir": ".cline/skills",
    },
    "gemini": {
        "name": "Gemini CLI",
        "global_dir": "~/.gemini/skills",
        "local_dir": ".gemini/skills",
    },
    "zed": {
        "name": "Zed",
        "global_dir": "~/.config/zed/skills",
        "local_dir": ".zed/skills",
    },
}

CATEGORY_EMOJIS = {
    "ai-agents": "🤖",
    "ai-development": "🧠",
    "ai-enhancers": "⚡",
    "content-media": "🎨",
    "data-ml": "📊",
    "devops": "🛠️",
    "documentation": "📝",
    "education": "📚",
    "integrations": "🔗",
    "productivity": "🚀",
    "prompts": "💬",
    "skill-tools": "🔧",
    "testing": "🧪",
    "utilities": "📦",
}


def api_get(endpoint: str, params: Optional[dict] = None, retries: int = 3) -> Optional[dict]:
    url = f"{API_BASE}{endpoint}"
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=15,
                                headers={"User-Agent": "SkillHub/1.0"})
            if resp.status_code == 200:
                try:
                    return resp.json()
                except ValueError:
                    if attempt < retries - 1:
                        continue
                    return None
            elif attempt < retries - 1:
                continue
            else:
                return None
        except requests.RequestException:
            if attempt < retries - 1:
                continue
            return None


def format_stars(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def truncate(s: str, max_len: int = 80) -> str:
    return s[:max_len] + "..." if len(s) > max_len else s


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    console.print(Panel.fit(
        "[bold cyan]🛒 SkillHub[/] — [yellow]AI Agent Skills Marketplace[/]\n"
        "[dim]Browse, search, download & install skills from SkillsMP (221k+ skills)[/]",
        border_style="cyan"
    ))


def resolve_path(path_str: str) -> Path:
    return Path(os.path.expanduser(path_str))


def get_agent_install_dir(agent_key: str, global_install: bool = True, cwd: str = ".") -> Path:
    agent = AGENTS.get(agent_key)
    if not agent:
        return None
    dir_key = "global_dir" if global_install else "local_dir"
    path_str = agent[dir_key]
    if not global_install:
        path_str = os.path.join(cwd, path_str)
    return resolve_path(path_str)


def fetch_trending() -> list:
    data = api_get("/stats")
    if not data:
        return []
    return data.get("trending", [])


def fetch_recent() -> list:
    data = api_get("/stats")
    if not data:
        return []
    return data.get("recent", [])


def fetch_stats() -> Optional[dict]:
    return api_get("/stats")


def fetch_categories() -> list:
    data = api_get("/stats")
    if not data:
        return []
    return list(data.get("categoryCounts", {}).items())


def fetch_top_authors() -> list:
    data = api_get("/stats")
    if not data:
        return []
    return data.get("topAuthors", [])


def search_skills(query: str, limit: int = 50, offset: int = 0, category: str = None) -> dict:
    # Try server-side search first
    params = {"search": query, "limit": limit, "offset": offset}
    if category:
        params["category"] = category
    data = api_get("/skills", params)
    if data and data.get("skills"):
        return data
    # If search API fails (returns 500), fall back to fetching all and filtering locally
    data = api_get("/skills", params={"limit": 100, "offset": offset})
    if data and data.get("skills"):
        all_skills = data["skills"]
        ql = query.lower()
        filtered = [
            s for s in all_skills
            if ql in s.get("scopedName", "").lower()
            or ql in s.get("description", "").lower()
            or ql in s.get("author", "").lower()
            or ql in s.get("name", "").lower()
        ]
        if category:
            filtered = [s for s in filtered if s.get("category") == category]
        return {"skills": filtered[:limit], "total": len(filtered)}
    return {"skills": [], "total": 0}


def fetch_skill_detail(scoped_name: str) -> Optional[dict]:
    # Try exact match via name filter first (limit high to get many results)
    data = api_get("/skills", params={"limit": 50})
    if data and data.get("skills"):
        for s in data["skills"]:
            if s.get("scopedName") == scoped_name:
                return s
    # Fall back to search
    name = scoped_name.replace("@", "").replace("/", " ")
    data = api_get("/skills", params={"search": name, "limit": 10})
    if data and data.get("skills"):
        for s in data["skills"]:
            if s.get("scopedName") == scoped_name:
                return s
        return data["skills"][0]
    return None


def resolve_raw_url(skill: dict) -> Optional[str]:
    raw_url = skill.get("rawUrl", "")
    if raw_url and raw_url not in ("none", ""):
        return raw_url
    repo = skill.get("repoFullName", "")
    path = skill.get("path", "")
    if repo and path:
        path_part = path.strip("/")
        # path may already include SKILL.md or just the directory
        if not path_part.endswith("SKILL.md"):
            path_part = path_part.rstrip("/") + "/SKILL.md"
        for branch in ("main", "master"):
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path_part}"
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    return url
            except:
                continue
    return None


def download_skill_content(skill: dict) -> Optional[str]:
    url = resolve_raw_url(skill)
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=10,
                            headers={"User-Agent": "SkillHub/1.0"})
        if resp.status_code == 200:
            return resp.text
    except:
        pass
    return None


def install_skill_to_agent(skill_name: str, skill_content: str, agent_key: str,
                           global_install: bool = True, cwd: str = ".") -> bool:
    agent = AGENTS.get(agent_key)
    if not agent:
        return False

    install_dir = get_agent_install_dir(agent_key, global_install, cwd)
    if not install_dir:
        return False

    skill_dir = install_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_content)

    return True


def show_skill_card(skill: dict, index: int = None) -> Panel:
    name = skill.get("scopedName", skill.get("name", "Unknown"))
    desc = truncate(skill.get("description", "No description"), 70)
    author = skill.get("author", "Unknown")
    stars = skill.get("stars", 0)
    category = skill.get("category", "")
    cat_emoji = CATEGORY_EMOJIS.get(category, "📌")

    header = f"[bold cyan]{name}[/]"
    if index is not None:
        header = f"[dim]{index}.[/] {header}"

    content = Group(
        Text(desc, style="white"),
        Text(f"👤 {author}  ⭐ {format_stars(stars)}  {cat_emoji} {category or 'uncategorized'}",
             style="dim"),
    )
    return Panel(content, title=header, border_style="blue", padding=(0, 1), width=70)


def show_skill_detail(skill: dict):
    clear_screen()
    print_header()

    name = skill.get("scopedName", skill.get("name", "Unknown"))
    desc = skill.get("description", "No description")
    author = skill.get("author", "Unknown")
    stars = skill.get("stars", 0)
    forks = skill.get("forks", 0)
    category = skill.get("category", "")
    repo = skill.get("repoFullName", "")
    path = skill.get("path", "")
    has_content = skill.get("hasContent", False)
    github_url = skill.get("githubUrl", "")

    cat_emoji = CATEGORY_EMOJIS.get(category, "📌")

    info = Table.grid(padding=(0, 2))
    info.add_column(style="bold yellow")
    info.add_column(style="white")
    info.add_row("Name:", name)
    info.add_row("Description:", desc)
    info.add_row("Author:", f"👤 {author}")
    info.add_row("Rating:", f"⭐ {format_stars(stars)} stars  🍴 {format_stars(forks)} forks")
    info.add_row("Category:", f"{cat_emoji} {category}" if category else "N/A")
    info.add_row("Repository:", repo)
    info.add_row("Path:", path)

    console.print(Panel(info, title=f"[bold cyan]{name}[/]", border_style="cyan"))
    print()

    console.print("[bold]Actions:[/]")
    console.print("  [1] 📥 Download/View SKILL.md content")
    console.print("  [2] 💾 Install to agent(s)")
    console.print("  [3] 🔗 Open GitHub URL")
    console.print("  [0] ↩️  Back")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", choices=["0", "1", "2", "3"], default="0")

    if choice == "1":
        with Progress(SpinnerColumn(), TextColumn("[yellow]Downloading...[/]"), transient=True) as p:
            p.add_task("", total=None)
            content = download_skill_content(skill)

        if content:
            console.print(Panel(
                Syntax(content, "markdown", theme="monokai", word_wrap=True),
                title=f"[bold green]{name} — SKILL.md[/]",
                border_style="green"
            ))
        else:
            console.print("[yellow]No downloadable content found or skill has no SKILL.md[/]")

        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        show_skill_detail(skill)

    elif choice == "2":
        install_skill_flow(skill)

    elif choice == "3":
        if github_url:
            console.print(f"[blue]{github_url}[/]")
            console.print("[dim]Copy the URL above and open in browser[/]")
        else:
            console.print("[yellow]No GitHub URL available[/]")
        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        show_skill_detail(skill)


def install_skill_flow(skill: dict):
    name = skill.get("scopedName", skill.get("name", "Unknown"))

    clear_screen()
    print_header()
    console.print(Panel.fit(f"[bold cyan]Installing: {name}[/]", border_style="cyan"))
    print()

    content = download_skill_content(skill)
    if not content:
        console.print("[red]Failed to download skill content[/]")
        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        return

    console.print("[bold]Select install location:[/]")
    console.print("  [1] 🌐 Global (~/.config/opencode/skills/, ~/.claude/skills/, etc.)")
    console.print("  [2] 📁 Local (project-level .opencode/skills/, .claude/skills/, etc.)")
    loc_choice = Prompt.ask("[bold cyan]Location[/]", choices=["1", "2"], default="1")
    global_install = loc_choice == "1"

    console.print("\n[bold]Select target agent(s):[/]")
    agent_keys = list(AGENTS.keys())
    for i, (key, agent) in enumerate(AGENTS.items(), 1):
        console.print(f"  [{i}] {agent['name']}")
    console.print(f"  [a] All agents")
    console.print(f"  [d] Done selecting")
    print()

    selected = []
    while True:
        choice = Prompt.ask("[bold cyan]Add agent[/]",
                            choices=[str(i) for i in range(1, len(agent_keys) + 1)] + ["a", "d"],
                            default="d")
        if choice == "d":
            break
        elif choice == "a":
            selected = agent_keys[:]
            break
        else:
            idx = int(choice) - 1
            agent_key = agent_keys[idx]
            if agent_key not in selected:
                selected.append(agent_key)
                console.print(f"  [green]✓[/] Added {AGENTS[agent_key]['name']}")
            else:
                console.print(f"  [yellow]Already selected[/]")

    if not selected:
        console.print("[yellow]No agents selected. Installation cancelled.[/]")
        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        return

    cwd = os.getcwd()
    success_count = 0
    fail_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task("[cyan]Installing...", total=len(selected))
        for agent_key in selected:
            agent_name = AGENTS[agent_key]["name"]
            try:
                install_skill_to_agent(name, content, agent_key, global_install, cwd)
                progress.console.print(f"  [green]✓[/] Installed to {agent_name}")
                success_count += 1
            except Exception as e:
                progress.console.print(f"  [red]✗[/] Failed to install to {agent_name}: {e}")
                fail_count += 1
            progress.update(task, advance=1)

    print()
    console.print(Panel(
        f"[green]Successfully installed to {success_count} agent(s)[/]"
        + (f"\n[yellow]{fail_count} failure(s)[/]" if fail_count else ""),
        border_style="green" if fail_count == 0 else "yellow"
    ))
    print()
    console.print(Prompt.ask("[dim]Press Enter to continue...[/]", default=""))
    return


def menu_trending():
    clear_screen()
    print_header()

    with Progress(SpinnerColumn(), TextColumn("[yellow]Loading trending skills...[/]"), transient=True) as p:
        p.add_task("", total=None)
        trending = fetch_trending()
        stats = fetch_stats()

    if stats:
        total = stats.get("stats", {}).get("totalSkills", 0)
        authors = stats.get("stats", {}).get("uniqueAuthors", 0)
        console.print(
            f"[dim]SkillsMP: {total:,} skills from {authors:,} authors[/]\n")

    if not trending:
        console.print("[red]Failed to load trending skills[/]")
        console.print("\n[dim]Press Enter to return...[/]")
        input()
        return

    table = Table(title="🔥 Trending Skills", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Skill", style="cyan", no_wrap=True)
    table.add_column("Author", style="yellow")
    table.add_column("⭐ Stars", justify="right")
    table.add_column("Description")

    for i, skill in enumerate(trending[:20], 1):
        name = skill.get("scopedName", skill.get("name", "Unknown"))
        author = skill.get("author", "Unknown")
        stars = format_stars(skill.get("stars", 0))
        desc = truncate(skill.get("description", ""), 50)
        table.add_row(str(i), name, author, stars, desc)

    console.print(table)
    print()

    console.print("[bold]Options:[/]")
    console.print("  [1-20] View skill details")
    console.print("  [r] Refresh")
    console.print("  [0] Back to main menu")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", default="0")
    if choice == "0":
        return
    elif choice == "r":
        menu_trending()
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(trending):
                show_skill_detail(trending[idx])
                menu_trending()
        except (ValueError, IndexError):
            pass


def menu_recent():
    clear_screen()
    print_header()

    with Progress(SpinnerColumn(), TextColumn("[yellow]Loading recent skills...[/]"), transient=True) as p:
        p.add_task("", total=None)
        recent = fetch_recent()

    if not recent:
        console.print("[red]Failed to load recent skills[/]")
        console.print("\n[dim]Press Enter to return...[/]")
        input()
        return

    table = Table(title="🆕 Recent Skills", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Skill", style="cyan", no_wrap=True)
    table.add_column("Author", style="yellow")
    table.add_column("⭐ Stars", justify="right")
    table.add_column("Description")

    for i, skill in enumerate(recent[:20], 1):
        name = skill.get("scopedName", skill.get("name", "Unknown"))
        author = skill.get("author", "Unknown")
        stars = format_stars(skill.get("stars", 0))
        desc = truncate(skill.get("description", ""), 50)
        table.add_row(str(i), name, author, stars, desc)

    console.print(table)
    print()

    console.print("[bold]Options:[/]")
    console.print("  [1-20] View skill details")
    console.print("  [r] Refresh")
    console.print("  [0] Back to main menu")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", default="0")
    if choice == "0":
        return
    elif choice == "r":
        menu_recent()
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(recent):
                show_skill_detail(recent[idx])
                menu_recent()
        except (ValueError, IndexError):
            pass


def menu_search():
    clear_screen()
    print_header()

    query = Prompt.ask("[bold cyan]🔍 Search skills[/]")
    if not query.strip():
        return

    category_choice = Prompt.ask("[bold cyan]Category filter[/] (press Enter to skip)", default="")
    category = category_choice.strip() or None

    with Progress(SpinnerColumn(), TextColumn(f"[yellow]Searching for '{query}'...[/]"), transient=True) as p:
        p.add_task("", total=None)
        result = search_skills(query, limit=50, category=category)

    skills = result.get("skills", [])
    total = result.get("total", 0)

    console.print(f"\n[bold]Found {total:,} skills for '{query}'[/]")
    if not skills:
        console.print("[yellow]No results[/]")
        console.print("\n[dim]Press Enter to return...[/]")
        input()
        return

    console.print()

    for i, skill in enumerate(skills[:20], 1):
        show_skill_card(skill, i)
        print()

    if total > 20:
        console.print(f"[dim]... and {total - 20} more results[/]")
        print()

    console.print("[bold]Options:[/]")
    console.print("  [1-20] View skill details")
    console.print("  [s] New search")
    console.print("  [0] Back to main menu")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", default="0")
    if choice == "0":
        return
    elif choice == "s":
        menu_search()
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(skills):
                show_skill_detail(skills[idx])
                menu_search()
        except (ValueError, IndexError):
            pass


def menu_categories():
    clear_screen()
    print_header()

    with Progress(SpinnerColumn(), TextColumn("[yellow]Loading categories...[/]"), transient=True) as p:
        p.add_task("", total=None)
        categories = fetch_categories()

    if not categories:
        console.print("[red]Failed to load categories[/]")
        console.print("\n[dim]Press Enter to return...[/]")
        input()
        return

    table = Table(title="📂 Skill Categories", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Category", style="cyan")
    table.add_column("Skills", justify="right")

    sorted_cats = sorted(categories, key=lambda x: x[1], reverse=True)
    for i, (cat, count) in enumerate(sorted_cats, 1):
        emoji = CATEGORY_EMOJIS.get(cat, "📌")
        table.add_row(str(i), f"{emoji} {cat}", f"{count:,}")

    console.print(table)
    print()

    console.print("[bold]Options:[/]")
    console.print("  [1-14] Browse skills in category")
    console.print("  [0] Back to main menu")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", default="0")
    if choice == "0":
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sorted_cats):
                cat_name = sorted_cats[idx][0]
                browse_category(cat_name)
        except (ValueError, IndexError):
            pass


def browse_category(category: str):
    clear_screen()
    print_header()
    cat_emoji = CATEGORY_EMOJIS.get(category, "📌")
    console.print(f"[bold]{cat_emoji} Category: {category}[/]\n")

    with Progress(SpinnerColumn(),
                  TextColumn(f"[yellow]Loading skills in '{category}'...[/]"),
                  transient=True) as p:
        p.add_task("", total=None)
        result = search_skills("", limit=50, category=category)

    skills = result.get("skills", [])
    total = result.get("total", 0)

    console.print(f"[dim]{total:,} skills in this category[/]\n")

    if not skills:
        console.print("[yellow]No skills loaded (API limitation)[/]")
        console.print("\n[dim]Press Enter to return...[/]")
        input()
        return

    for i, skill in enumerate(skills[:20], 1):
        show_skill_card(skill, i)
        print()

    console.print("[bold]Options:[/]")
    console.print("  [1-20] View skill details")
    console.print("  [s] Search within category")
    console.print("  [0] Back to categories")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", default="0")
    if choice == "0":
        menu_categories()
        return
    elif choice == "s":
        query = Prompt.ask("[bold cyan]Search in category[/]")
        if query.strip():
            with Progress(SpinnerColumn(),
                          TextColumn(f"[yellow]Searching...[/]"),
                          transient=True) as p:
                p.add_task("", total=None)
                result = search_skills(query, limit=50, category=category)
            skills = result.get("skills", [])
            if skills:
                for i, s in enumerate(skills[:20], 1):
                    show_skill_card(s, i)
                    print()
            else:
                console.print("[yellow]No results[/]")
            console.print("\n[dim]Press Enter to continue...[/]")
            input()
            browse_category(category)
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(skills):
                show_skill_detail(skills[idx])
                browse_category(category)
        except (ValueError, IndexError):
            pass


def menu_top_authors():
    clear_screen()
    print_header()

    with Progress(SpinnerColumn(), TextColumn("[yellow]Loading top authors...[/]"), transient=True) as p:
        p.add_task("", total=None)
        authors = fetch_top_authors()

    if not authors:
        console.print("[red]Failed to load top authors[/]")
        console.print("\n[dim]Press Enter to return...[/]")
        input()
        return

    table = Table(title="🏆 Top Authors", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Author", style="cyan")
    table.add_column("Skills", justify="right")

    for i, author in enumerate(authors[:20], 1):
        table.add_row(str(i), author.get("name", "Unknown"),
                      str(author.get("skillCount", 0)))

    console.print(table)
    console.print("\n[dim]Press Enter to return...[/]")
    input()


def menu_installed():
    clear_screen()
    print_header()

    console.print("[bold cyan]📋 Installed Skills Manager[/]\n")

    table = Table(box=box.SIMPLE, header_style="bold cyan")
    table.add_column("Agent", style="yellow")
    table.add_column("Directory", style="dim")
    table.add_column("Status")

    for key, agent in AGENTS.items():
        gdir = resolve_path(agent["global_dir"])
        gcount = len(list(gdir.glob("*/SKILL.md"))) if gdir.exists() else 0

        ldir = Path.cwd() / agent["local_dir"]
        lcount = len(list(ldir.glob("*/SKILL.md"))) if ldir.exists() else 0

        status_parts = []
        if gcount > 0:
            status_parts.append(f"[green]{gcount} global[/]")
        if lcount > 0:
            status_parts.append(f"[blue]{lcount} local[/]")
        status = status_parts[0] if status_parts else "[dim]none[/]"

        table.add_row(agent["name"], str(gdir), status)

    console.print(table)
    print()

    console.print("[bold]Options:[/]")
    console.print("  [1] List installed skills for OpenCode")
    console.print("  [2] Remove installed skill")
    console.print("  [0] Back to main menu")
    print()

    choice = Prompt.ask("[bold cyan]Choose[/]", choices=["0", "1", "2"], default="0")

    if choice == "1":
        opencode_dir = resolve_path(AGENTS["opencode"]["global_dir"])
        if opencode_dir.exists():
            skills = sorted(opencode_dir.glob("*/SKILL.md"))
            if skills:
                console.print(f"\n[bold]OpenCode skills ({len(skills)}):[/]")
                for s in skills:
                    console.print(f"  • [cyan]{s.parent.name}[/]")
            else:
                console.print("\n[yellow]No skills installed for OpenCode[/]")
        else:
            console.print("\n[yellow]OpenCode skills directory not found[/]")
        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        menu_installed()

    elif choice == "2":
        name = Prompt.ask("[bold cyan]Skill name to remove[/]")
        if name:
            removed = False
            for key, agent in AGENTS.items():
                for is_global in [True, False]:
                    d = get_agent_install_dir(key, is_global)
                    skill_path = d / name
                    if skill_path.exists():
                        shutil.rmtree(skill_path)
                        console.print(f"  [red]✗[/] Removed from {agent['name']}")
                        removed = True
            if not removed:
                console.print("[yellow]Skill not found in any agent directory[/]")
        console.print("\n[dim]Press Enter to continue...[/]")
        input()
        menu_installed()


def main():
    while True:
        clear_screen()
        print_header()

        stats_data = fetch_stats()
        if stats_data:
            s = stats_data.get("stats", {})
            total = s.get("totalSkills", 0)
            authors = s.get("uniqueAuthors", 0)
            console.print(
                f"[dim]📊 {total:,} skills  ·  {authors:,} authors  ·  "
                f"{len(stats_data.get('categoryCounts', {}))} categories[/]\n"
            )

        menu = Table.grid(padding=(0, 2))
        menu.add_column(style="bold yellow", width=4)
        menu.add_column(style="white")
        menu.add_row("[1]", "🔥 Trending Skills")
        menu.add_row("[2]", "🆕 Recent Skills")
        menu.add_row("[3]", "🔍 Search Skills")
        menu.add_row("[4]", "📂 Browse Categories")
        menu.add_row("[5]", "🏆 Top Authors")
        menu.add_row("[6]", "📋 Installed Skills Manager")
        menu.add_row("[7]", "❓ About")
        menu.add_row("[0]", "[dim]Exit[/]")

        console.print(Panel(menu, title="[bold]Main Menu[/]", border_style="cyan"))
        print()

        choice = Prompt.ask("[bold cyan]Choose[/]",
                            choices=["0", "1", "2", "3", "4", "5", "6", "7"],
                            default="0")

        if choice == "0":
            console.print("[yellow]Goodbye![/]")
            break
        elif choice == "1":
            menu_trending()
        elif choice == "2":
            menu_recent()
        elif choice == "3":
            menu_search()
        elif choice == "4":
            menu_categories()
        elif choice == "5":
            menu_top_authors()
        elif choice == "6":
            menu_installed()
        elif choice == "7":
            clear_screen()
            console.print(Panel.fit(
                "[bold cyan]SkillHub[/] - AI Agent Skills Marketplace Client\n\n"
                "Version 1.0\n"
                "Data source: [link=https://agentskills.in]agentskills.in[/] (SkillsMP)\n\n"
                "[bold]Features:[/]\n"
                "• Browse 221k+ skills from SkillsMP\n"
                "• Search and filter by category\n"
                "• View trending and recent skills\n"
                "• Download SKILL.md content\n"
                "• Install to 9 AI agents:\n"
                "  OpenCode, Claude Code, Cursor, Copilot,\n"
                "  Codex, Windsurf, Cline, Gemini CLI, Zed\n\n"
                "[dim]Data provided by SkillsMP / agentskills.in[/]",
                border_style="cyan", title="About"
            ))
            print()
            console.print("[dim]Press Enter to return...[/]")
            input()
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/]")
        sys.exit(0)
