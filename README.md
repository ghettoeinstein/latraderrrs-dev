# latraderrrs-dev

Source for **latraderrrs.com** — static site deployed via GitHub Pages.

## Workflow (regular push/edit)

```bash
cd ~/latraderrrs.com

# 1. Edit files (index.html, etc.)

# 2. Commit + push
git add -A
git commit -m "Describe the change"
git push

# 3. GitHub Pages auto-deploys within ~30 seconds.
#    No build step — plain HTML/CSS/JS served as-is.
```

**Live URLs:**
- Production (custom domain): https://latraderrrs.com
- Fallback (github.io): https://ghettoeinstein.github.io/latraderrrs-dev/

## Structure

```
latraderrrs.com/
├── index.html   # Single-file landing page (500 lines, self-contained)
├── CNAME        # Custom domain pointer (latraderrrs.com) — auto-managed by Pages
└── README.md
```

## Important

- **Do NOT delete the `CNAME` file** — it's what points latraderrrs.com at this repo.
- Pushes to `main` deploy automatically. No preview/staging branch configured.
- DNS for latraderrrs.com is on Cloudflare (104.21.69.230, 172.67.215.109 — Cloudflare proxies).
  If you ever move off Cloudflare, point the apex A records at GitHub's IPs:
  `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.

## Repo

- Private-to-public flipped for Pages (free plan requires public).
- Remote uses **HTTPS** (gh CLI token), not SSH — SSH keys aren't registered on this machine.
