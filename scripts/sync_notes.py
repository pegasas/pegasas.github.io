#!/usr/bin/env python3
"""Sync pegasas-notes-v2 into this Jekyll site (GitHub Pages friendly).

Design
------
* Additive only: everything generated lives under ``notes/`` (owned by this
  script).  Nothing outside ``notes/`` is touched, so all original pages stay.
* Source of truth stays in pegasas-notes-v2; the site holds a rendered mirror.
* Incremental: ``notes/.sync-manifest.json`` records a hash per generated file.
  Re-running only rewrites changed files and deletes files whose source is gone.
  Hand edits inside ``notes/`` are therefore overwritten -- edit the source.
* GitHub Pages runs Jekyll 3.9 without custom plugins, so everything Jekyll
  cannot do (link rewriting, Liquid escaping, front matter, index pages) is
  done here at sync time.

Usage
-----
  python3 scripts/sync_notes.py --source ~/pegasas-notes-v2          # sync
  python3 scripts/sync_notes.py --source ... --check                 # exit 1 if stale
  python3 scripts/sync_notes.py --source ... --dry-run               # show plan
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

SITE_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR_NAME = "notes"
MANIFEST_NAME = ".sync-manifest.json"
GITHUB_BLOB = "https://github.com/pegasas/pegasas-notes-v2/blob/main/"
GITHUB_TREE = "https://github.com/pegasas/pegasas-notes-v2/tree/main/"

# (source path, output prefix under notes/).  Directories are walked for *.md.
DEFAULT_INCLUDES = [
    ("knowledge", ""),                     # knowledge/x/y.md -> notes/x/y/
    ("company-ecosystems", "company-ecosystems"),
    ("KNOWLEDGE_ARCHITECTURE.md", "architecture.md"),
]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")
REFDEF_RE = re.compile(r"^(\s{0,3}\[[^\]]+\]:\s*)(\S+)", re.M)
HTML_SRC_RE = re.compile(r"""(<(?:img|a)\b[^>]*?\b(?:src|href)=)(["'])([^"']+)\2""", re.I)
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Sync:
    def __init__(self, source: Path, out: Path, baseurl: str, only: str = ""):
        self.only = only.strip("/")
        self.titles: dict[str, str] = {}
        self.source = source
        self.out = out
        self.baseurl = baseurl.rstrip("/")
        self.md_map: dict[Path, str] = {}   # source md (abs) -> site url path
        self.outputs: dict[str, bytes] = {}  # rel path under site root -> bytes

    # ---- planning -------------------------------------------------------
    def collect(self, includes):
        for src_rel, prefix in includes:
            src = self.source / src_rel
            if src.is_file() and src.suffix == ".md":
                self._plan_md(src, Path(prefix))
            elif src.is_dir():
                for p in sorted(src.rglob("*.md")):
                    rel = p.relative_to(src)
                    if any(part.startswith((".", "_")) for part in rel.parts):
                        continue  # Jekyll ignores these anyway
                    self._plan_md(p, Path(prefix) / rel)

    def _plan_md(self, src: Path, rel_out: Path):
        if self.only and not src.relative_to(self.source).as_posix().startswith(self.only):
            return  # --only: pilot a subset; links to the rest fall back to GitHub
        if rel_out.name.lower() == "readme.md":
            url_parts = list(rel_out.parent.parts)
            out_file = Path(OUT_DIR_NAME, *url_parts, "index.md")
        else:
            url_parts = list(rel_out.with_suffix("").parts)
            out_file = Path(OUT_DIR_NAME, *rel_out.parts)
        url = "/" + "/".join([OUT_DIR_NAME, *url_parts]) + "/"
        self.md_map[src.resolve()] = url
        self._plan = getattr(self, "_plan", [])
        self._plan.append((src, out_file, url))

    # ---- conversion -----------------------------------------------------
    def build(self):
        for src, out_file, url in self._plan:
            text = src.read_text(encoding="utf-8", errors="replace")
            self.outputs[out_file.as_posix()] = self.convert(src, text, url).encode()

    def convert(self, src: Path, text: str, url: str) -> str:
        text = text.replace("\r\n", "\n")
        if text.startswith("---\n"):  # drop pre-existing front matter
            end = text.find("\n---\n", 4)
            if end != -1:
                text = text[end + 5:]
        title, body = self._split_title(text, src)
        self.titles[url] = title
        body = self._rewrite_links(body, src)
        needs_math = "$$" in body or re.search(r"(?<!\\)\$[^\s$][^$\n]*\$", body) is not None
        needs_mermaid = "```mermaid" in body
        body = self._escape_liquid(body)
        rel_src = src.relative_to(self.source).as_posix()
        fm = [
            "---",
            "layout: single",
            "classes: wide",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"permalink: {url}",
            "author_profile: false",
            "breadcrumbs: true",
            "toc: true",
            "toc_sticky: true",
            f"source_path: {json.dumps(rel_src)}",
            f"source_url: {json.dumps(GITHUB_BLOB + quote(rel_src))}",
        ]
        if needs_math:
            fm.append("math: true")
        if needs_mermaid:
            fm.append("mermaid: true")
        fm.append("---\n")
        return "\n".join(fm) + "\n" + body.lstrip("\n")

    @staticmethod
    def _split_title(text: str, src: Path):
        lines = text.split("\n")
        in_fence = False
        for i, line in enumerate(lines):
            if FENCE_RE.match(line):
                in_fence = not in_fence
            if not in_fence and line.startswith("# "):
                title = line[2:].strip().strip("#").strip()
                del lines[i]  # layout renders the title
                return title or src.stem, "\n".join(lines)
            if not in_fence and line.strip() and not line.lstrip().startswith("<!--"):
                break
        return src.stem.replace("-", " ").replace("_", " "), "\n".join(lines)

    def _resolve(self, target: str, src: Path) -> str:
        """Map a relative link target to a site URL / asset URL / GitHub URL."""
        if re.match(r"^([a-z][a-z0-9+.-]*:|//|#|/|\{\{)", target, re.I):
            return target
        path, sep, anchor = target.partition("#")
        path = path.split("?")[0]
        if not path:
            return target
        if len(path) > 240:  # prose accidentally inside (...), not a path
            return target
        dest = (src.parent / path).resolve()
        try:
            dest.relative_to(self.source.resolve())
            dest.exists()
        except (ValueError, OSError):
            return target
        anchor = sep + anchor if sep else ""
        if dest.is_dir():
            readme = next((c for c in (dest / "README.md", dest / "readme.md") if c.exists()), None)
            if readme and readme.resolve() in self.md_map:
                return self.baseurl + self.md_map[readme.resolve()] + anchor
            return GITHUB_TREE + quote(dest.relative_to(self.source.resolve()).as_posix()) + anchor
        if dest in self.md_map:
            return self.baseurl + self.md_map[dest] + anchor
        if dest.suffix.lower() in IMAGE_EXTS and dest.exists():
            return self.baseurl + self._copy_image(dest) + anchor
        if dest.exists():
            return GITHUB_BLOB + quote(dest.relative_to(self.source.resolve()).as_posix()) + anchor
        return target  # dangling in the source repo; leave untouched

    def _copy_image(self, dest: Path) -> str:
        rel = dest.relative_to(self.source.resolve()).as_posix()
        if rel.startswith("knowledge/"):
            rel = rel[len("knowledge/"):]
        key = f"{OUT_DIR_NAME}/{rel}"
        self.outputs[key] = dest.read_bytes()
        return "/" + key

    def _rewrite_links(self, body: str, src: Path) -> str:
        out, in_fence = [], False
        for line in body.split("\n"):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                out.append(line)
                continue
            if in_fence:
                out.append(line)
                continue
            # split on inline code so we never rewrite inside `...`
            parts = re.split(r"(`+[^`]*`+)", line)
            for i in range(0, len(parts), 2):
                seg = parts[i]
                seg = LINK_RE.sub(lambda m: m.group(1) + self._resolve(m.group(2), src) + m.group(3), seg)
                seg = HTML_SRC_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{self._resolve(m.group(3), src)}{m.group(2)}", seg)
                parts[i] = seg
            out.append("".join(parts))
        body = "\n".join(out)
        return REFDEF_RE.sub(lambda m: m.group(1) + self._resolve(m.group(2), src), body)

    @staticmethod
    def _escape_liquid(body: str) -> str:
        if "{{" not in body and "{%" not in body:
            return body
        body = body.replace("{% endraw %}", "{% endraw %}{{ '{% endraw %}' }}{% raw %}")
        return "{% raw %}\n" + body + "\n{% endraw %}\n"

    # ---- index ----------------------------------------------------------
    def add_landing(self):
        key = f"{OUT_DIR_NAME}/index.md"
        if key in self.outputs:
            return
        dirs = sorted({Path(k).parts[1] for k in self.outputs
                       if k.endswith("/index.md") and len(Path(k).parts) == 3})
        if dirs:
            items = "\n".join(f"- [{d}]({self.baseurl}/{OUT_DIR_NAME}/{d}/)" for d in dirs)
        else:  # pilot mode: list the synced pages directly
            items = "\n".join(f"- [{t}]({self.baseurl}{u})" for u, t in sorted(self.titles.items()))
        self.outputs[key] = (
            "---\nlayout: single\nclasses: wide\ntitle: \"已同步页面\"\npermalink: /notes/all/\n"
            "author_profile: false\n---\n\n"
            "从 pegasas-notes-v2 同步到本站的页面。按分类浏览见 [Notes]({{ '/notes/' | relative_url }})。\n\n" + items + "\n"
        ).encode()

    # ---- apply ----------------------------------------------------------
    def apply(self, dry_run: bool):
        manifest_path = self.out / MANIFEST_NAME
        old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        new = {k: sha(v) for k, v in self.outputs.items()}
        write = [k for k, h in new.items() if old.get(k) != h or not (SITE_ROOT / k).exists()]
        delete = [k for k in old if k not in new]
        stats = {"files": len(new), "written": len(write), "deleted": len(delete)}
        if dry_run:
            return stats, write, delete
        for k in write:
            p = SITE_ROOT / k
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(self.outputs[k])
        for k in delete:
            p = SITE_ROOT / k
            if p.is_file() and Path(k).parts[0] == OUT_DIR_NAME:  # never leave notes/
                p.unlink()
        for d in sorted((p for p in self.out.rglob("*") if p.is_dir()), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
        self.out.mkdir(exist_ok=True)
        manifest_path.write_text(json.dumps(new, indent=0, sort_keys=True) + "\n")
        return stats, write, delete


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=os.environ.get("NOTES_SOURCE", str(Path.home() / "pegasas-notes-v2")))
    ap.add_argument("--baseurl", default="", help="site baseurl (empty for pegasas.github.io)")
    ap.add_argument("--only", default="", help="sync only source paths with this prefix, e.g. knowledge/algorithm/docs/01-basic/01-amortized-analysis.md")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check", action="store_true", help="exit 1 when notes/ is out of date")
    args = ap.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not (source / "knowledge").is_dir():
        print(f"error: {source} does not look like pegasas-notes-v2", file=sys.stderr)
        return 2
    s = Sync(source, SITE_ROOT / OUT_DIR_NAME, args.baseurl, args.only)
    s.collect(DEFAULT_INCLUDES)
    s.build()
    s.add_landing()
    stats, write, delete = s.apply(dry_run=args.dry_run or args.check)
    print(json.dumps(stats))
    if args.dry_run or args.check:
        for k in write[:20]:
            print("  would write", k)
        for k in delete[:20]:
            print("  would delete", k)
    return 1 if args.check and (write or delete) else 0


if __name__ == "__main__":
    sys.exit(main())
