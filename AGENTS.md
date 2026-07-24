# foid-report — agent instructions

Read **POSTING.md** in this repo root for the full posting workflow across
foid.report / fringe.report / intervals.report.

The short version:
- Post text goes up **verbatim** — never rewrite, fix, or restyle it.
- A markdown file landing in `posts/YYYY-MM-DD.md` on `main` IS the publish;
  a GitHub Action rebuilds the site. No PRs, straight to `main`.
- Never delete posts (undo = move to `drafts/`). Never post to
  intervals.report — it is autonomous.
