# foid-report

Static generator for [foid.report](https://foid.report). Black page, white text, big masthead. No dependencies — same pattern as scene-log.

## Posting

1. Add a markdown file to `posts/` named by date: `posts/2026-07-05.md`
   (two posts same day: `posts/2026-07-05-two.md`)
2. Optional frontmatter:

   ```
   ---
   title: the report title
   ---
   ```

   Or just start with `# a title`, or nothing — the date becomes the title.
3. Build and publish:

   ```
   python3 build.py
   git add -A && git commit -m "post" && git push
   ```

GitHub Pages serves `docs/` on `main`. `drafts/` is ignored by the build.
