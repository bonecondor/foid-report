# foid-report

Static blog generator for foid.report. GitHub Pages serves the `docs/` folder on the `main` branch — nothing is live until it lands on `main`.

## How to publish a post (the ONLY workflow — do not improvise)

When the user gives you post text to upload:

1. Save the text VERBATIM to `posts/YYYY-MM-DD.md` using today's date
   (second post same day: `posts/YYYY-MM-DD-two.md`). Do not rewrite,
   "fix", or restyle the user's prose — lowercase, typos, and quirks are
   intentional. Only add markdown links the user explicitly asks for,
   e.g. `[word](https://intervals.report)`.
2. Run `python3 build.py` from the repo root. It regenerates `docs/`.
   Confirm it prints "built N post(s)".
3. Commit the new post AND the regenerated `docs/` files together,
   message `post: YYYY-MM-DD`.
4. Push so the commit reaches `main` (if you are required to work on a
   feature branch, push the branch, then fast-forward merge to `main`
   and push `main` — with the user's OK). The post is not live until
   `main` has it.

Notes:
- No frontmatter needed; a bare paragraph is a valid post (date becomes the title).
- `drafts/` is ignored by the build.
- The user often asks to link one word to https://intervals.report or https://fringe.report — link exactly the occurrence(s) they specify.
- Do not create pull requests for posts unless asked; posts go straight to `main`.
