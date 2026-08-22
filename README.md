# SCU Cyber Security Knowledge Base

Mockup knowledge base for Southern Cross University cyber security content.
Static site built from markdown → deployed to Cloudflare Pages.

## Editing content

1. Edit markdown files in `content/` — these are the source articles.
2. Add new articles to `content.json` under `articles`.
3. Run `python build.py` to regenerate `dist/`.
4. Push to `main` — GitHub Actions deploys automatically.

## Structure

```
content/          ← Edit these markdown files (the actual content)
  mfa-overview.md
  register-passkey.md
  setup-authenticator.md
  setup-totp.md
content.json      ← Article metadata, nav, ordering
templates/        ← HTML templates (SCU design)
assets/           ← CSS, images, fonts
build.py          ← Static site generator
dist/             ← Built HTML (gitignored, built by CI)
```

## Design tokens (from live scu.edu.au)

| Token | Value |
|---|---|
| Primary (Gold) | #FFDC4B |
| Secondary (Navy) | #084E74 |
| Text | #032436 |
| Sage | #E4EFEE |
| Headings | Montserrat 600 |
| Body | "Graphik Web" → system font fallback |
| Border | #EDF3F6 |
| Logo | /assets/scu-logo.png (from live site)