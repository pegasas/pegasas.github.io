#!/usr/bin/env python3
"""Generate assets/images/profile/github-stats.svg and top-langs.svg from the GitHub API.

Replaces the (unreliable) github-readme-stats.vercel.app images. Needs GITHUB_TOKEN with
repo scope to include private repos; falls back to public data without it.
Usage: GITHUB_TOKEN=... python3 scripts/gen_github_stats.py [--user pegasas]
"""
import argparse, json, os, sys, urllib.request, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets/images/profile"
TOK = os.environ.get("GITHUB_TOKEN", "")

def api(url, data=None):
    req = urllib.request.Request(url if url.startswith("http") else "https://api.github.com" + url,
                                 data=json.dumps(data).encode() if data else None,
                                 headers={"Authorization": f"Bearer {TOK}"} if TOK else {})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def gql(q):
    return api("/graphql", {"query": q})["data"]

def collect(user):
    repos, page = [], 1
    while True:
        chunk = api(f"/user/repos?per_page=100&affiliation=owner&visibility=all&page={page}") if TOK \
            else api(f"/users/{user}/repos?per_page=100&page={page}")
        repos += chunk
        if len(chunk) < 100: break
        page += 1
    own = [r for r in repos if not r["fork"]]
    prof = api(f"/users/{user}")
    created = int(prof["created_at"][:4]); now = datetime.date.today().year
    commits = 0
    for y in range(created, now + 1):
        d = gql('{user(login:"%s"){contributionsCollection(from:"%d-01-01T00:00:00Z",to:"%d-12-31T23:59:59Z"){totalCommitContributions restrictedContributionsCount}}}' % (user, y, y))
        c = d["user"]["contributionsCollection"]; commits += c["totalCommitContributions"] + c["restrictedContributionsCount"]
    g = gql('{user(login:"%s"){pullRequests{totalCount} issues{totalCount} repositoriesContributedTo(first:1,contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}}}' % user)["user"]
    def langs(r):
        try: return api(r["languages_url"])
        except Exception: return {}
    with ThreadPoolExecutor(8) as ex: per = list(ex.map(langs, own))
    tot = {}
    for l in per:
        for k, v in l.items(): tot[k] = tot.get(k, 0) + v
    return dict(stars=sum(r["stargazers_count"] for r in own), commits=commits, prs=g["pullRequests"]["totalCount"],
                issues=g["issues"]["totalCount"], contrib=g["repositoriesContributedTo"]["totalCount"],
                repos=len(own), followers=prof["followers"], langs=tot)

FONT = '-apple-system,BlinkMacSystemFont,&quot;Segoe UI&quot;,Inter,Helvetica,Arial,sans-serif'
def frame(w, h, label, eyebrow, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
<defs>
<radialGradient id="ga" cx="0%" cy="0%" r="60%"><stop offset="0" stop-color="#7bd43c" stop-opacity=".22"/><stop offset="1" stop-color="#7bd43c" stop-opacity="0"/></radialGradient>
<radialGradient id="gb" cx="100%" cy="100%" r="60%"><stop offset="0" stop-color="#3d9bff" stop-opacity=".22"/><stop offset="1" stop-color="#3d9bff" stop-opacity="0"/></radialGradient>
<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="#7bd43c" stop-opacity="0"/><stop offset=".3" stop-color="#7bd43c"/><stop offset=".65" stop-color="#3d9bff"/><stop offset="1" stop-color="#ff7a1f" stop-opacity="0"/></linearGradient>
<clipPath id="r"><rect width="{w}" height="{h}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#r)" font-family="{FONT}">
<rect width="{w}" height="{h}" fill="#07080b"/><rect width="{w}" height="{h}" fill="url(#ga)"/><rect width="{w}" height="{h}" fill="url(#gb)"/>
<rect y="{h-2}" width="{w}" height="2" fill="url(#ln)"/>
<text x="32" y="46" font-size="12" font-weight="800" letter-spacing="2.5" fill="#7bd43c">{eyebrow}</text>
<text x="32" y="78" font-size="24" font-weight="900" fill="#fff">{title}</text>
{body}
</g></svg>
'''

def stats_svg(s):
    items = [("Commits", s["commits"], "#7bd43c"), ("Pull requests", s["prs"], "#ff7a1f"), ("Issues", s["issues"], "#3d9bff"),
             ("Stars earned", s["stars"], "#9a6bff"), ("Repositories", s["repos"], "#7bd43c"), ("Followers", s["followers"], "#ff7a1f")]
    body = ""
    for i, (k, v, c) in enumerate(items):
        x = 32 + (i % 3) * 196; y = 124 + (i // 3) * 92
        body += f'<rect x="{x}" y="{y}" width="180" height="76" rx="14" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".09"/>' \
                f'<rect x="{x}" y="{y}" width="180" height="3" rx="1.5" fill="{c}"/>' \
                f'<text x="{x+18}" y="{y+42}" font-size="28" font-weight="900" fill="{c}">{v:,}</text>' \
                f'<text x="{x+18}" y="{y+63}" font-size="13" font-weight="600" fill="#98a2b3">{k}</text>'
    return frame(620, 320, "GitHub stats", "ACTIVITY", "GitHub Stats", body)

COL = ["#7bd43c", "#ff7a1f", "#3d9bff", "#9a6bff", "#3fe0c5", "#f2c14e", "#e5557a", "#98a2b3"]
def langs_svg(s):
    items = sorted(s["langs"].items(), key=lambda kv: -kv[1])[:8]
    total = sum(v for _, v in items) or 1
    body = '<clipPath id="bar"><rect x="32" y="102" width="556" height="12" rx="6"/></clipPath><g clip-path="url(#bar)">'
    x = 32.0
    for i, (k, v) in enumerate(items):
        w = 556 * v / total; body += f'<rect x="{x:.1f}" y="102" width="{w:.1f}" height="12" fill="{COL[i]}"/>'; x += w
    body += '</g>'
    for i, (k, v) in enumerate(items):
        cx = 32 + (i % 2) * 280; cy = 150 + (i // 2) * 34
        body += f'<circle cx="{cx+6}" cy="{cy-5}" r="6" fill="{COL[i]}"/><text x="{cx+20}" y="{cy}" font-size="14" font-weight="700" fill="#e9edf4">{k}</text>' \
                f'<text x="{cx+248}" y="{cy}" text-anchor="end" font-size="14" font-weight="800" fill="#98a2b3">{100*v/total:.1f}%</text>'
    return frame(620, 320, "Most used languages", "LANGUAGES", "Most Used Languages", body)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--user", default="pegasas"); a = ap.parse_args()
    s = collect(a.user)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "github-stats.svg").write_text(stats_svg(s)); (OUT / "top-langs.svg").write_text(langs_svg(s))
    print({k: v for k, v in s.items() if k != "langs"}, sorted(s["langs"].items(), key=lambda kv: -kv[1])[:8])
