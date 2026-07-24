# How to post — foid.report / fringe.report / intervals.report

Canonical posting guide. Lives in both blog repos; identical copies:
- https://raw.githubusercontent.com/bonecondor/foid-report/main/POSTING.md
- https://raw.githubusercontent.com/bonecondor/fringe-report/main/POSTING.md

Hand this file to any Claude / Codex / agent on any computer and it has
everything it needs.

## The three sites

| site | repo | what it is |
|---|---|---|
| foid.report | bonecondor/foid-report | black-on-white blog, longer posts |
| fringe.report | bonecondor/fringe-report | paper/typewriter notes stream, numbered dispatches (FR 0001…), optional tags |
| intervals.report | bonecondor/intervals-report | **autonomous. NEVER post to it manually. Never touch published posts or timestamps.** It is only ever a link *target*. |

## Cardinal rules

1. **Post text goes up VERBATIM.** Never rewrite, fix typos, restyle,
   capitalize, or "improve" the prose. Lowercase and quirks are intentional.
2. Only add markdown links explicitly asked for. Common request: link one
   word to https://intervals.report or https://fringe.report — link exactly
   the occurrence(s) specified, nothing else.
3. Never delete a post. "Undo" = move it to `drafts/` and republish.
   (Repos are public — undone posts remain in git history.)
4. Posts go straight to `main`. No PRs, no feature branches, unless asked.

## The one thing to know

**A markdown file landing in `posts/` on `main` IS the publish.**
Each repo has a GitHub Action (`.github/workflows/build.yml`) that rebuilds
the site on push. No local build needed. Pages redeploys in ~1–2 minutes.

## Post format (both sites)

- Filename: `posts/YYYY-MM-DD.md` (today's date).
  Second post same day: `posts/YYYY-MM-DD-two.md` or a time suffix like
  `posts/YYYY-MM-DD-2216.md` — anything that keeps filenames unique and sorted.
- Frontmatter is entirely optional; a bare paragraph is a valid post
  (the date becomes the title). Include `time:` when you can — posts are
  dated by filename only.

foid frontmatter:

    ---
    title: the report title
    time: 7:00 PM
    ---

fringe frontmatter (tags are free-form; each tag gets a page at /tag/<tag>.html):

    ---
    title: what the post is about
    tags: person, musing
    time: 9:05 pm
    ---

## Ways to post, easiest first

### 1. From a phone or any browser — the drop page
https://bonecondor.github.io/drop/ — black half posts to foid, green half
to fringe. Needs the fine-grained GitHub PAT pasted in once per device
(repo access: foid-report + fringe-report only, Contents read/write).

### 2. From any computer with git (no clone needed beforehand)

    git clone --depth 1 https://github.com/bonecondor/foid-report   # or fringe-report
    cd foid-report
    cat > posts/2026-07-24.md <<'EOF'
    ---
    time: 7:00 PM
    ---
    the post text, verbatim
    EOF
    git add posts/ && git commit -m "post: 2026-07-24" && git push

Done — the Action builds the site. (Auth: whatever GitHub credentials that
machine has for bonecondor; `gh auth login` if none.)

### 3. GitHub web UI (no terminal at all)
github.com/bonecondor/foid-report → `posts/` → Add file → Create new file →
paste → Commit directly to main.

### 4. On the home Mac — full local path
Repos live at `~/Documents/Code/Projects/foid-report` and `…/fringe-report`.
Optionally build locally to preview:

    python3 build.py    # regenerates docs/, prints "built N post(s)"
    git add -A && git commit -m "post: YYYY-MM-DD" && git pull --rebase && git push

(Committing `docs/` locally is fine — the Action is a no-op if docs/ is
already current.) The Blog Drop app (always-on :8377) also posts locally.

## Verifying / troubleshooting

- Live check: https://foid.report / https://fringe.report (hard-refresh).
- Not updating after ~2 min → check the repo's Actions tab for a failed
  `build` run. Pages serves `docs/` on `main`; nothing is live until
  `main` has it.
- `drafts/` is ignored by the build on both sites.
