import os
import re
import requests

HTB_TOKEN = os.environ["HTB_API_TOKEN"]
HTB_ID = os.environ["HTB_PROFILE_ID"]


def fetch_htb():
    url = f"https://labs.hackthebox.com/api/v4/user/profile/basic/{HTB_ID}"
    headers = {"Authorization": f"Bearer {HTB_TOKEN}", "Accept": "application/json"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()["profile"]


def build_table(p):
    rows = [
        ("Rank", p.get("rank")),
        ("Points", p.get("points")),
        ("Global Ranking", f"#{p.get('ranking')}"),
        ("User Owns", p.get("user_owns")),
        ("System Owns", p.get("system_owns")),
        ("Respects", p.get("respects")),
    ]
    lines = ["| Stat | Value |", "|------|-------|"]
    for label, value in rows:
        lines.append(f"| {label} | {value} |")
    return "\n".join(lines)


def update_readme(table):
    path = "README.md"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    start, end = "<!--START_SECTION:htb-stats-->", "<!--END_SECTION:htb-stats-->"
    block = f"{start}\n{table}\n{end}"

    if start in content and end in content:
        content = re.sub(f"{start}.*?{end}", block, content, flags=re.S)
    else:
        content += f"\n\n{block}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    profile = fetch_htb()
    update_readme(build_table(profile))
