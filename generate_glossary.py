#!/usr/bin/env python3
"""
LA Traders Glossary Generator — programmatic SEO
Generates: /glossary/index.html + /glossary/<slug>/index.html per term
Plus: sitemap.xml, llms.txt, robots.txt

Usage: python3 generate_glossary.py
Source of truth: glossary_terms.json — edit terms THERE, then re-run.
"""
import json, os, datetime, html as htmllib

BASE = "https://latraderrrs.com"
TODAY = datetime.date.today().isoformat()
OUT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(OUT, "glossary_terms.json")) as f:
    TERMS = json.load(f)

BY_SLUG = {t["slug"]: t for t in TERMS}
CATS = {}
for t in TERMS:
    CATS.setdefault(t["category"], []).append(t)

CAT_ORDER = ["RRR Framework", "Market Structure", "Liquidity", "Price Action",
             "Sessions & Time", "Risk & Execution", "Instruments", "Options"]

def esc(s):
    return htmllib.escape(s, quote=True)

CSS = """
/* Glossary-specific styles only.
   Design tokens, base, buttons, cards, chips, nav, footer
   come from /assets/latraders.css (design system). */
.wrap{max-width:var(--wrap-narrow);}
.crumb{margin:48px 0 10px;}
.cat-tag{margin-bottom:20px;}
h1{font-size:clamp(34px,5.4vw,54px);margin-bottom:20px;}
.short{font-size:var(--text-lg);color:var(--ash);line-height:1.6;max-width:640px;margin-bottom:48px;padding-left:20px;border-left:2px solid var(--gold-dim);}
h2{font-weight:400;font-size:24px;margin:44px 0 14px;}
h2 .num{font-family:var(--font-mono);font-size:var(--text-xs);color:var(--gold);letter-spacing:2px;display:block;margin-bottom:8px;text-transform:uppercase;}
p{font-size:var(--text-base);line-height:1.75;margin-bottom:14px;}
.example-box{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:10px;padding:24px 26px;margin:22px 0;}
.example-box .label{font-family:var(--font-mono);font-size:10px;letter-spacing:2px;color:var(--gold);text-transform:uppercase;margin-bottom:10px;}
.example-box p{font-size:14.5px;margin:0;font-style:italic;}
.related{margin-top:56px;padding-top:32px;border-top:1px solid var(--line);}
.related h3{font-family:var(--font-display);font-weight:400;font-size:18px;margin-bottom:18px;color:var(--ash);}
.cta-band{margin-top:64px;}
"""

INDEX_CSS = """
.hero-g{padding:80px 0 56px;text-align:left;}
.hero-g h1{margin-bottom:16px;}
.hero-g .sub{font-size:var(--text-md);color:var(--ash);max-width:600px;}
.stat-row{display:flex;gap:28px;margin-top:28px;font-family:var(--font-mono);font-size:var(--text-xs);letter-spacing:2px;text-transform:uppercase;color:var(--ash-dim);}
.stat-row b{color:var(--gold);font-weight:400;}
.cat-block{margin-bottom:64px;}
.cat-title{font-family:var(--font-display);font-weight:400;font-size:22px;color:var(--bone);margin-bottom:22px;padding-bottom:12px;border-bottom:1px solid var(--line);}
.term-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.term-card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius-md);padding:22px 24px;transition:all var(--dur-fast) var(--ease-out);}
.term-card:hover{border-color:var(--gold-dim);background:var(--panel-2);transform:translateY(-2px);}
.term-name{font-family:var(--font-display);font-size:17px;font-weight:600;color:var(--bone);margin-bottom:8px;}
.term-card:hover .term-name{color:var(--gold-bright);}
.term-short{font-size:var(--text-sm);color:var(--ash);line-height:1.55;}
@media(max-width:720px){.term-grid{grid-template-columns:1fr;}}
"""

def head(title, desc, canonical, extra_schema="", extra_css=""):
    # Shared design system from site root — works on latraderrrs.com and on
    # local `python3 -m http.server` run from the repo root.
    css_href = "/assets/latraders.css"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="LA Traders">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_href}">
<style>{CSS}{extra_css}</style>
{extra_schema}
</head>
<body>
<nav class="nav-shell">
  <a class="nav-brand" href="/">LA TRADERS</a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/glossary/">Glossary</a>
    <a href="/#checklist">Checklist</a>
    <a href="/#oslite">RRR OS Lite</a>
  </div>
</nav>
"""

def foot():
    # Fortune-20 mega footer: brand block + 4 link columns + legal bar + risk disclosure
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-mega">
      <div class="footer-brandblock">
        <div class="fbrand">
          <img src="/assets/lion.jpg" alt="LA Traders lion mark">
          <span>LA TRADERS</span>
        </div>
        <p class="fmission">One repeatable process for the New York session. No noise. No hopium. Just structure.</p>
        <div class="fmeta">
          Los Angeles, California<br>
          Futures &amp; Options Education<br>
          Est. New York Open, Every Session
        </div>
      </div>
      <div class="fcol">
        <h4>The System</h4>
        <ul>
          <li><a href="/#protocol">The 6:00 AM Protocol</a></li>
          <li><a href="/#rrr">RRR Framework</a></li>
          <li><a href="/glossary/rrr-framework/">Reveal &rarr; Retrace &rarr; Run</a></li>
          <li><a href="/glossary/a-plus-setup/">The A+ Setup</a></li>
        </ul>
      </div>
      <div class="fcol">
        <h4>Education</h4>
        <ul>
          <li><a href="/glossary/">Trading Glossary</a></li>
          <li><a href="/glossary/market-structure/">Market Structure</a></li>
          <li><a href="/glossary/liquidity/">Liquidity Concepts</a></li>
          <li><a href="/glossary/risk-to-reward/">Risk Management</a></li>
        </ul>
      </div>
      <div class="fcol">
        <h4>Products</h4>
        <ul>
          <li><a href="/#checklist">RRR Daily Checklist — Free</a></li>
          <li><a href="/#oslite">RRR OS Lite — $17</a></li>
          <li><a href="/glossary/prop-firm/">Prop Firm Path</a></li>
          <li><a href="/glossary/journaling/">Trade Journaling</a></li>
        </ul>
      </div>
      <div class="fcol">
        <h4>Company</h4>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/glossary/">Glossary</a></li>
          <li><a href="/glossary/discipline/">Our Discipline</a></li>
          <li><a href="/glossary/new-york-session/">The Session We Trade</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-legal">
      <div class="fcopy">&copy; LA Traders &mdash; All Rights Reserved</div>
      <div class="flinks">
        <a href="/">Home</a>
        <a href="/glossary/">Glossary</a>
        <a href="/#protocol">Protocol</a>
        <a href="/#rrr">RRR Framework</a>
        <a href="/#checklist">Checklist</a>
      </div>
    </div>
    <div class="footer-risk">
      <p><strong>RISK DISCLOSURE:</strong> Futures and options trading involves substantial risk of loss and is not suitable for every investor. The valuation of futures and options may fluctuate, and as a result, clients may lose more than their original investment. Past performance is not indicative of future results. LA Traders provides education and community only &mdash; nothing on this site constitutes financial advice, a solicitation, or a recommendation to buy or sell any security or futures contract. You are solely responsible for your own trading decisions.</p>
    </div>
  </div>
</footer>
</body>
</html>"""

def ldjson(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def build_term_page(t):
    canonical = f"{BASE}/glossary/{t['slug']}/"
    title = f"What is {t['term']}? — LA Traders Glossary"
    schema = ldjson({
        "@context": "https://schema.org", "@type": "DefinedTerm",
        "name": t["term"], "description": t["short"],
        "inDefinedTermSet": BASE + "/glossary/", "url": canonical,
    }) + ldjson({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"What is {t['term']} in trading?",
             "acceptedAnswer": {"@type": "Answer", "text": t["short"]}},
            {"@type": "Question", "name": f"Why does {t['term']} matter for day traders?",
             "acceptedAnswer": {"@type": "Answer", "text": t["why"]}},
            {"@type": "Question", "name": f"What is an example of {t['term']}?",
             "acceptedAnswer": {"@type": "Answer", "text": t["example"]}},
        ],
    })
    chips = []
    seen = set()
    for r in t["related"]:
        rt = BY_SLUG.get(r)
        if rt and r not in seen:
            seen.add(r)
            chips.append(f'<a class="chip" href="/glossary/{r}/">{esc(rt["term"])}</a>')
    for x in CATS[t["category"]]:
        if x["slug"] != t["slug"] and x["slug"] not in seen and len(chips) < 8:
            seen.add(x["slug"])
            chips.append(f'<a class="chip" href="/glossary/{x["slug"]}/">{esc(x["term"])}</a>')

    body = f"""<div class="wrap">
  <div class="crumb"><a href="/">Home</a> / <a href="/glossary/">Glossary</a> / {esc(t["term"])}</div>
  <div class="cat-tag">{esc(t["category"])}</div>
  <h1>What is <em>{esc(t["term"])}</em>?</h1>
  <p class="short">{esc(t["short"])}</p>

  <h2><span class="num">The Definition</span>{esc(t["term"])}, defined</h2>
  <p>{esc(t["definition"])}</p>

  <h2><span class="num">Why It Matters</span>Why {esc(t["term"])} matters</h2>
  <p>{esc(t["why"])}</p>

  <h2><span class="num">In Practice</span>{esc(t["term"])} — a real example</h2>
  <div class="example-box">
    <div class="label">Example · New York Session</div>
    <p>{esc(t["example"])}</p>
  </div>

  <div class="related">
    <h3>Related terms</h3>
    <div class="chips">{"".join(chips)}</div>
  </div>

  <div class="cta-band">
    <h3>Learn the full system</h3>
    <p>The RRR Daily Trading Checklist — the exact morning routine LA Traders runs before every New York session. Free.</p>
    <a class="btn" href="/#checklist">Get the Free Checklist</a>
  </div>
</div>
"""
    return head(title, t["short"], canonical, schema) + body + foot()

def build_index():
    canonical = f"{BASE}/glossary/"
    title = "Trading Glossary — RRR Framework, Liquidity, Market Structure & More | LA Traders"
    desc = "Every trading term that matters, defined the LA Traders way: the RRR framework, liquidity concepts, market structure, price action, risk management, futures and options — with real New York session examples."
    schema = ldjson({
        "@context": "https://schema.org", "@type": "DefinedTermSet",
        "name": "LA Traders Glossary", "description": desc, "url": canonical,
        "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t["term"],
                            "url": f"{BASE}/glossary/{t['slug']}/"} for t in TERMS],
    })
    sections = []
    for cat in CAT_ORDER:
        terms = CATS.get(cat, [])
        if not terms:
            continue
        cards = "".join(
            f"""<a class="term-card" href="/glossary/{t['slug']}/">
    <div class="term-name">{esc(t['term'])}</div>
    <div class="term-short">{esc(t['short'])}</div>
  </a>""" for t in terms)
        sections.append(f"""<div class="cat-block">
  <h2 class="cat-title">{esc(cat)}</h2>
  <div class="term-grid">{cards}</div>
</div>""")
    body = f"""<div class="wrap">
  <div class="hero-g">
    <div class="crumb" style="margin:0 0 10px;"><a href="/">Home</a> / Glossary</div>
    <h1>The <em>Trading Glossary</em></h1>
    <p class="sub">Every term that matters, defined the LA Traders way — no textbook filler, just what each concept means at 6:30 AM when the New York open prints.</p>
    <div class="stat-row"><span><b>{len(TERMS)}</b> terms</span><span><b>{len(CATS)}</b> categories</span><span>Updated {TODAY}</span></div>
  </div>
  {"".join(sections)}
  <div class="cta-band">
    <h3>Learn the full system</h3>
    <p>The RRR Daily Trading Checklist — the exact morning routine LA Traders runs before every New York session. Free.</p>
    <a class="btn" href="/#checklist">Get the Free Checklist</a>
  </div>
</div>"""
    return head(title, desc, canonical, schema, INDEX_CSS) + body + foot()

# ---------- Build ----------
os.makedirs(os.path.join(OUT, "glossary"), exist_ok=True)
urls = ["/", "/glossary/"]

with open(os.path.join(OUT, "glossary", "index.html"), "w") as f:
    f.write(build_index())
print("Built glossary index")

for t in TERMS:
    d = os.path.join(OUT, "glossary", t["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(build_term_page(t))
    urls.append(f"/glossary/{t['slug']}/")
print(f"Built {len(TERMS)} term pages")

# sitemap.xml
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pri = "1.0" if u == "/" else ("0.9" if u == "/glossary/" else "0.8")
    sm.append(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>')
sm.append("</urlset>")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write("\n".join(sm))
print(f"sitemap.xml: {len(urls)} URLs")

# robots.txt
robots = f"""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {BASE}/sitemap.xml
"""
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(robots)
print("robots.txt written")

# llms.txt
cat_lines = []
for cat in CAT_ORDER:
    terms = CATS.get(cat, [])
    if not terms:
        continue
    cat_lines.append(f"## {cat}")
    for t in terms:
        cat_lines.append(f"- {t['term']}: {t['short']} ({BASE}/glossary/{t['slug']}/)")
    cat_lines.append("")
llms = f"""# LA Traders — Trading education built on one repeatable process
# Los Angeles, CA · Futures & Options · New York session specialists

LA Traders teaches one repeatable process for the New York session (for every session):
mark the levels, wait for the reveal, take the A+ setup. No noise. No hopium. Just structure.
The core methodology is the RRR Framework (Reveal → Retrace → Run), executed through the
6:00 AM Protocol: mark the overnight range, 4H structure, 1H structure, overnight midpoint,
and the NY opening candle — then trade only A+ setups with defined risk.

## Key Pages
- {BASE}/ — Homepage: the RRR framework, the 6:00 AM Protocol, free checklist, RRR OS Lite ($17)
- {BASE}/glossary/ — Full trading glossary ({len(TERMS)} terms, {len(CATS)} categories)

## Products
- RRR Daily Trading Checklist: Free. The exact morning routine before every NY session.
- RRR OS Lite: $17 one-time. Complete playbook, chart templates, A+ criteria, community access.

## Glossary ({len(TERMS)} terms)
{chr(10).join(cat_lines)}
## AI Crawler Allowlist
- GPTBot: Allow
- ClaudeBot: Allow
- PerplexityBot: Allow
- Google-Extended: Allow
"""
with open(os.path.join(OUT, "llms.txt"), "w") as f:
    f.write(llms)
print("llms.txt written")
print("DONE")
