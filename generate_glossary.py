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

/* Protocol callout box */
.protocol-callout{margin:36px 0;border-radius:14px;padding:28px 30px;position:relative;overflow:hidden;}
.protocol-callout::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;}
.protocol-callout.pc-blue{background:rgba(54,97,201,0.08);border:1px solid rgba(54,97,201,0.2);}
.protocol-callout.pc-blue::before{background:var(--blue);}
.protocol-callout.pc-purple{background:rgba(124,79,196,0.08);border:1px solid rgba(124,79,196,0.2);}
.protocol-callout.pc-purple::before{background:var(--purple);}
.protocol-callout.pc-red{background:rgba(195,61,46,0.08);border:1px solid rgba(195,61,46,0.2);}
.protocol-callout.pc-red::before{background:var(--red);}
.protocol-callout.pc-white{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);}
.protocol-callout.pc-white::before{background:var(--bone);}
.protocol-callout.pc-gold{background:var(--gold-glow);border:1px solid var(--gold-dim);}
.protocol-callout.pc-gold::before{background:var(--gold);}
.protocol-callout .pc-label{font-family:var(--font-mono);font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;display:flex;align-items:center;gap:8px;}
.protocol-callout .pc-icon{width:8px;height:8px;border-radius:50%;display:inline-block;}
.protocol-callout.pc-blue .pc-label{color:#6b8ad6;}
.protocol-callout.pc-blue .pc-icon{background:var(--blue);}
.protocol-callout.pc-purple .pc-label{color:var(--purple-bright);}
.protocol-callout.pc-purple .pc-icon{background:var(--purple);}
.protocol-callout.pc-red .pc-label{color:#e06b5a;}
.protocol-callout.pc-red .pc-icon{background:var(--red);}
.protocol-callout.pc-white .pc-label{color:var(--bone);}
.protocol-callout.pc-white .pc-icon{background:var(--bone);}
.protocol-callout.pc-gold .pc-label{color:var(--gold-bright);}
.protocol-callout.pc-gold .pc-icon{background:var(--gold);}
.protocol-callout .pc-stage{font-family:var(--font-display);font-weight:400;font-size:15px;color:var(--bone);margin-bottom:8px;}
.protocol-callout .pc-text{font-size:14.5px;line-height:1.7;color:var(--bone-dim);margin:0;}
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
<nav class="nav-shell mega-nav">
  <a class="nav-brand" href="/">LA TRADERS</a>
  <div class="nav-links mega-links">
    <div class="mega-item">
      <a href="/#protocol">The System</a>
      <div class="mega-dropdown">
        <div class="mega-col">
          <h5>The Process</h5>
          <ul>
            <li><a href="/#protocol">The 6:00 AM Protocol</a></li>
            <li><a href="/#rrr">RRR Framework</a></li>
            <li><a href="/glossary/a-plus-setup/">The A+ Setup</a></li>
            <li><a href="/glossary/six-am-protocol/">6:00 AM Protocol</a></li>
          </ul>
        </div>
        <div class="mega-col">
          <h5>RRR Framework</h5>
          <ul>
            <li><a href="/glossary/rrr-framework/">RRR Framework</a></li>
            <li><a href="/glossary/reveal/">Reveal</a></li>
            <li><a href="/glossary/retrace/">Retrace</a></li>
            <li><a href="/glossary/run/">Run</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="mega-item">
      <a href="/glossary/">Glossary</a>
      <div class="mega-dropdown mega-wide">
        <div class="mega-col"><h5>RRR Framework</h5><ul>
          <li><a href="/glossary/rrr-framework/">RRR Framework</a></li>
          <li><a href="/glossary/reveal/">Reveal</a></li>
          <li><a href="/glossary/retrace/">Retrace</a></li>
          <li><a href="/glossary/run/">Run</a></li>
          <li><a href="/glossary/a-plus-setup/">A+ Setup</a></li>
          <li><a href="/glossary/six-am-protocol/">6:00 AM Protocol</a></li>
        </ul></div>
        <div class="mega-col"><h5>Market Structure</h5><ul>
          <li><a href="/glossary/market-structure/">Market Structure</a></li>
          <li><a href="/glossary/break-of-structure/">Break of Structure</a></li>
          <li><a href="/glossary/change-of-character/">Change of Character</a></li>
          <li><a href="/glossary/swing-high/">Swing High</a></li>
          <li><a href="/glossary/swing-low/">Swing Low</a></li>
          <li><a href="/glossary/trend/">Trend</a></li>
        </ul></div>
        <div class="mega-col"><h5>Liquidity</h5><ul>
          <li><a href="/glossary/liquidity/">Liquidity</a></li>
          <li><a href="/glossary/liquidity-sweep/">Liquidity Sweep</a></li>
          <li><a href="/glossary/buy-side-liquidity/">Buy-Side Liquidity</a></li>
          <li><a href="/glossary/sell-side-liquidity/">Sell-Side Liquidity</a></li>
          <li><a href="/glossary/stop-hunt/">Stop Hunt</a></li>
          <li><a href="/glossary/turtle-soup/">Turtle Soup</a></li>
        </ul></div>
        <div class="mega-col"><h5>Price Action</h5><ul>
          <li><a href="/glossary/order-block/">Order Block</a></li>
          <li><a href="/glossary/fair-value-gap/">Fair Value Gap</a></li>
          <li><a href="/glossary/imbalance/">Imbalance</a></li>
          <li><a href="/glossary/breaker-block/">Breaker Block</a></li>
          <li><a href="/glossary/mitigation/">Mitigation</a></li>
          <li><a href="/glossary/premium-discount/">Premium &amp; Discount</a></li>
        </ul></div>
        <div class="mega-col"><h5>Sessions &amp; Time</h5><ul>
          <li><a href="/glossary/overnight-range/">Overnight Range</a></li>
          <li><a href="/glossary/overnight-midpoint/">Overnight Midpoint</a></li>
          <li><a href="/glossary/opening-candle/">Opening Candle</a></li>
          <li><a href="/glossary/opening-range/">Opening Range</a></li>
          <li><a href="/glossary/new-york-session/">New York Session</a></li>
          <li><a href="/glossary/killzone/">Killzone</a></li>
        </ul></div>
        <div class="mega-col"><h5>Risk &amp; Execution</h5><ul>
          <li><a href="/glossary/risk-to-reward/">Risk-to-Reward</a></li>
          <li><a href="/glossary/position-sizing/">Position Sizing</a></li>
          <li><a href="/glossary/expectancy/">Expectancy</a></li>
          <li><a href="/glossary/drawdown/">Drawdown</a></li>
          <li><a href="/glossary/revenge-trading/">Revenge Trading</a></li>
          <li><a href="/glossary/journaling/">Trade Journaling</a></li>
        </ul></div>
        <div class="mega-col"><h5>Instruments</h5><ul>
          <li><a href="/glossary/es-futures/">ES Futures</a></li>
          <li><a href="/glossary/nq-futures/">NQ Futures</a></li>
          <li><a href="/glossary/tick-value/">Tick Value</a></li>
          <li><a href="/glossary/margin/">Margin</a></li>
          <li><a href="/glossary/prop-firm/">Prop Firm</a></li>
        </ul></div>
        <div class="mega-col"><h5>Options</h5><ul>
          <li><a href="/glossary/options-contract/">Options Contract</a></li>
          <li><a href="/glossary/delta/">Delta</a></li>
          <li><a href="/glossary/theta/">Theta</a></li>
          <li><a href="/glossary/implied-volatility/">Implied Volatility</a></li>
        </ul></div>
      </div>
    </div>
    <div class="mega-item">
      <a href="/#checklist">Products</a>
      <div class="mega-dropdown">
        <div class="mega-col">
          <h5>Education &amp; Tools</h5>
          <ul>
            <li><a href="/tools/daily-checklist/">Interactive Checklist</a></li>
            <li><a href="/tools/position-size-calculator/">Position Size Calculator</a></li>
            <li><a href="/#checklist">Free PDF Checklist</a></li>
            <li><a href="/#oslite">RRR OS Lite — $17</a></li>
            <li><a href="/glossary/prop-firm/">Prop Firm Path</a></li>
            <li><a href="/glossary/journaling/">Trade Journaling</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="mega-item">
      <a href="/terms/">Legal</a>
      <div class="mega-dropdown">
        <div class="mega-col">
          <h5>Legal</h5>
          <ul>
            <li><a href="/terms/">Terms of Service</a></li>
            <li><a href="/privacy/">Privacy Policy</a></li>
          </ul>
        </div>
      </div>
    </div>
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
        <a href="/#protocol">Protocol</a>
        <a href="/#rrr">RRR Framework</a>
        <a href="/glossary/">Glossary</a>
        <a href="/#checklist">Checklist</a>
        <a href="/#oslite">RRR OS Lite</a>
        <a href="/terms/">Terms of Service</a>
        <a href="/privacy/">Privacy Policy</a>
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

    pf = t.get("protocol_fit", {})
    pf_color = pf.get("color", "gold")
    pf_stage = pf.get("stage", "The 6:00 AM Protocol")
    pf_text = pf.get("text", "Every term in the LA Traders system connects back to the 6:00 AM Protocol — the repeatable pre-market routine that structures every session.")

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

  <div class="protocol-callout pc-{pf_color}">
    <div class="pc-label"><span class="pc-icon"></span>How This Fits the 6:00 AM Protocol</div>
    <div class="pc-stage">{esc(pf_stage)}</div>
    <p class="pc-text">{esc(pf_text)}</p>
  </div>

  <div class="related">
    <h3>Related terms</h3>
    <div class="chips">{"".join(chips)}</div>
  </div>

  <div class="cta-band">
    <h3>Learn the full system</h3>
    <p>The RRR Daily Trading Checklist — the exact morning routine LA Traders runs before every New York session. Free.</p>
    <a class="btn" href="/tools/daily-checklist/">Open the Daily Checklist</a>
    <span style="margin:0 12px;color:var(--ash-dim);font-size:12px;">or</span>
    <a class="btn btn-ghost" href="/#checklist">Get the PDF Version</a>
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
    <a class="btn" href="/tools/daily-checklist/">Open the Interactive Checklist</a>
    <span style="margin:0 12px;color:var(--ash-dim);font-size:12px;">or</span>
    <a class="btn btn-ghost" href="/tools/position-size-calculator/">Position Size Calculator</a>
  </div>
</div>"""
    return head(title, desc, canonical, schema, INDEX_CSS) + body + foot()

# ---------- Build ----------
os.makedirs(os.path.join(OUT, "glossary"), exist_ok=True)
urls = ["/", "/glossary/", "/tools/", "/tools/daily-checklist/", "/tools/position-size-calculator/", "/tools/journal/"]

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
    pri = "1.0" if u == "/" else ("0.9" if u in ("/glossary/", "/tools/daily-checklist/") else ("0.8" if u.startswith("/glossary/") else "0.7"))
    sm.append(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pri}</priority></url>')
# Legal pages (low priority, yearly change)
for u in ["/terms/", "/privacy/"]:
    sm.append(f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>')
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


# ---------- LEGAL PAGES ----------
LEGAL_CSS = """
.legal-body{max-width:760px;}
.legal-body h1{margin-bottom:14px;}
.legal-updated{font-family:var(--font-mono);font-size:var(--text-xs);letter-spacing:2px;text-transform:uppercase;color:var(--ash-dim);margin-bottom:48px;}
.legal-body h2{font-size:20px;margin:40px 0 12px;font-weight:400;}
.legal-body h2 .num{color:var(--gold);font-family:var(--font-mono);font-size:var(--text-xs);letter-spacing:2px;display:block;margin-bottom:6px;}
.legal-body p{font-size:14.5px;line-height:1.75;color:var(--bone-dim);margin-bottom:12px;}
.legal-body ul{margin:10px 0 16px 22px;color:var(--bone-dim);font-size:14.5px;line-height:1.75;}
.legal-body li{margin-bottom:8px;}
.legal-body strong{color:var(--bone);font-weight:600;}
.legal-note{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:10px;padding:20px 24px;margin:20px 0;}
.legal-note p{margin:0;font-size:13.5px;font-style:italic;}
.toc{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius-md);padding:26px 30px;margin:32px 0 8px;}
.toc .toc-title{font-family:var(--font-mono);font-size:10px;letter-spacing:2px;color:var(--gold);text-transform:uppercase;margin-bottom:14px;}
.toc ol{margin-left:20px;color:var(--ash);font-size:13.5px;line-height:2;}
.toc a{color:var(--ash);transition:color var(--dur-fast);}
.toc a:hover{color:var(--gold);}
"""

TERMS_HTML = """<div class="wrap legal-body">
  <div class="crumb"><a href="/">Home</a> / Terms of Service</div>
  <h1>Terms of <em>Service</em></h1>
  <div class="legal-updated">Last Updated: __TODAY__ &middot; LA Traders &middot; Los Angeles, California</div>

  <div class="toc">
    <div class="toc-title">Contents</div>
    <ol>
      <li><a href="#acceptance">Acceptance of Terms</a></li>
      <li><a href="#education">Educational Content Only — No Financial Advice</a></li>
      <li><a href="#risk">Risk Disclosure</a></li>
      <li><a href="#accounts">Accounts &amp; Eligibility</a></li>
      <li><a href="#payments">Paid Products, Billing &amp; Refunds</a></li>
      <li><a href="#email">Email Marketing Communications</a></li>
      <li><a href="#sms">SMS / Text Message Program</a></li>
      <li><a href="#discord">Discord Community</a></li>
      <li><a href="#conduct">Acceptable Use &amp; Conduct</a></li>
      <li><a href="#ip">Intellectual Property</a></li>
      <li><a href="#thirdparty">Third-Party Platforms &amp; Links</a></li>
      <li><a href="#disclaimers">Disclaimers &amp; Limitation of Liability</a></li>
      <li><a href="#indemnity">Indemnification</a></li>
      <li><a href="#termination">Termination</a></li>
      <li><a href="#law">Governing Law &amp; Disputes</a></li>
      <li><a href="#changes">Changes to These Terms</a></li>
      <li><a href="#contact">Contact</a></li>
    </ol>
  </div>

  <h2 id="acceptance"><span class="num">Section 01</span>Acceptance of Terms</h2>
  <p>These Terms of Service ("Terms") govern your access to and use of latraderrrs.com, the LA Traders glossary and educational content, the RRR Daily Trading Checklist, RRR OS Lite, our email list, our SMS/text message program, and our Discord community (collectively, the "Services"), operated by LA Traders ("LA Traders," "we," "us," or "our").</p>
  <p>By accessing or using any of the Services — including downloading the checklist, purchasing a product, subscribing to emails or texts, or joining the Discord — you agree to be bound by these Terms and our <a href="/privacy/">Privacy Policy</a>. If you do not agree, do not use the Services.</p>

  <h2 id="education"><span class="num">Section 02</span>Educational Content Only — No Financial Advice</h2>
  <p><strong>Everything LA Traders publishes is education, not advice.</strong> All content — including the RRR framework, the 6:00 AM Protocol, glossary definitions, examples, chart markups, checklists, templates, Discord discussion, emails, and texts — is provided for general educational and informational purposes only.</p>
  <p>Nothing in the Services constitutes, or should be construed as:</p>
  <ul>
    <li>Financial, investment, legal, tax, or accounting advice;</li>
    <li>A recommendation, solicitation, or offer to buy or sell any security, futures contract, option, or other financial instrument;</li>
    <li>Personalized investment advice or a recommendation that any particular trade or strategy is suitable for you;</li>
    <li>A guarantee of any result, including passing any proprietary trading firm evaluation.</li>
  </ul>
  <p>We are not registered as an investment adviser, broker-dealer, or commodity trading advisor. You should consult a licensed financial professional before making any investment decision. <strong>You are solely responsible for your own trading decisions and their outcomes.</strong></p>

  <h2 id="risk"><span class="num">Section 03</span>Risk Disclosure</h2>
  <p><strong>Futures and options trading involves substantial risk of loss and is not suitable for every investor.</strong> You may lose more than your original investment. Leverage can work against you as well as for you. Past performance — ours or anyone's — is not indicative of future results.</p>
  <p>Hypothetical, simulated, or example performance (including any example trades in our content) has inherent limitations: it is prepared with hindsight, does not involve financial risk, and cannot account for the impact of real market conditions or your own discipline. No representation is being made that any account will or is likely to achieve profits or losses similar to those shown or discussed.</p>
  <p>Only trade with risk capital — money you can afford to lose without affecting your lifestyle or financial security.</p>

  <h2 id="accounts"><span class="num">Section 04</span>Accounts &amp; Eligibility</h2>
  <p>You must be at least 18 years old (or the age of majority in your jurisdiction) to use the Services. By using the Services, you represent that you meet this requirement and that any information you provide (name, email, phone number, Discord handle) is accurate and yours to provide.</p>
  <p>You are responsible for maintaining the confidentiality of any account credentials and for all activity under your accounts.</p>

  <h2 id="payments"><span class="num">Section 05</span>Paid Products, Billing &amp; Refunds</h2>
  <p>Certain products — including RRR OS Lite — are sold for a one-time fee displayed at checkout. Prices are in US dollars and may change at any time; the price you see at purchase is the price you pay.</p>
  <ul>
    <li><strong>Delivery:</strong> Digital products are delivered electronically to the email address you provide at checkout, typically within minutes.</li>
    <li><strong>Refunds:</strong> Unless otherwise stated at the point of sale, digital products may be refunded within 14 days of purchase if you are not satisfied — email <a href="mailto:support@latraderrrs.com">support@latraderrrs.com</a> with your order email. After delivery of substantial digital content, refund requests are reviewed case by case.</li>
    <li><strong>Taxes:</strong> You are responsible for any applicable sales or use taxes in your jurisdiction.</li>
    <li><strong>No subscriptions by default:</strong> If any recurring product is introduced, renewal terms, cancellation mechanics, and pricing will be disclosed before you are charged.</li>
  </ul>

  <h2 id="email"><span class="num">Section 06</span>Email Marketing Communications</h2>
  <p>When you provide your email address (for the free checklist, a purchase, or a signup), you consent to receive emails from LA Traders, including:</p>
  <ul>
    <li><strong>Transactional emails:</strong> delivery of your checklist or products, receipts, and support responses; and</li>
    <li><strong>Marketing emails:</strong> session notes, educational content, product announcements, and offers.</li>
  </ul>
  <p><strong>How to opt out:</strong> Every marketing email includes a one-click unsubscribe link in the footer. Clicking it removes you from marketing emails promptly (and in all cases within 10 business days, per CAN-SPAM). Transactional emails related to a purchase continue as needed to deliver what you bought. You can also email <a href="mailto:support@latraderrrs.com">support@latraderrrs.com</a> to be removed.</p>
  <p>We comply with the CAN-SPAM Act: accurate sender identity, honest subject lines, a functioning unsubscribe mechanism, and a valid physical contact address in every marketing email. We do not sell, rent, or share your email address with third parties for their own marketing.</p>

  <h2 id="sms"><span class="num">Section 07</span>SMS / Text Message Program</h2>
  <p>If you opt in to our SMS/text message program (for example, by texting a keyword to our number or submitting your phone number with SMS consent checked), the following terms apply:</p>
  <ul>
    <li><strong>Program description:</strong> LA Traders sends session-related and educational text messages, which may include pre-market protocol reminders, level-marking prompts, educational content, checklist delivery, and occasional product announcements.</li>
    <li><strong>Consent:</strong> Consent to receive marketing texts is not a condition of any purchase. By opting in, you expressly consent to receive recurring automated text messages (including via an automatic telephone dialing system) from or on behalf of LA Traders at the number you provided, consistent with the Telephone Consumer Protection Act (TCPA).</li>
    <li><strong>Message frequency:</strong> Varies; typically no more than 1 message per trading day, and most weeks fewer.</li>
    <li><strong>Message and data rates:</strong> Message and data rates may apply per your mobile carrier plan. Carriers are not liable for delayed or undelivered messages.</li>
    <li><strong>How to opt out:</strong> Reply <strong>STOP</strong> to any message to cancel at any time. You will receive one confirmation text, then no further messages unless you re-subscribe. For help, reply <strong>HELP</strong> or email <a href="mailto:support@latraderrrs.com">support@latraderrrs.com</a>.</li>
    <li><strong>Supported carriers:</strong> Major US carriers; availability may vary.</li>
  </ul>
  <p>We do not sell or share your mobile number with third parties for their marketing purposes. See our <a href="/privacy/">Privacy Policy</a> for how SMS data is handled.</p>

  <h2 id="discord"><span class="num">Section 08</span>Discord Community</h2>
  <p>Access to the LA Traders Discord server (the "Community") may be included with certain products or offered separately. The Community is a moderated educational space. By joining, you agree:</p>
  <ul>
    <li><strong>Your Discord account is yours:</strong> You are responsible for your Discord account and everything posted from it. Discord's own Terms of Service and Community Guidelines apply in addition to these Terms.</li>
    <li><strong>Community rules:</strong> No spam, self-promotion, or unsolicited DMs to members; no harassment, hate speech, or personal attacks; no posting of trade signals presented as advice ("calls to buy/sell"); no sharing of another member's private information; no redistribution of paid content (see Section 10).</li>
    <li><strong>Not advice, again:</strong> Discussion in the Community — including from moderators — is educational conversation, not financial advice. Screenshots and trade reviews shared in the Community are for learning, and may not reflect typical results.</li>
    <li><strong>Moderation:</strong> We may remove content, mute, suspend, or ban any member at our discretion to protect the Community. Severe or repeat violations result in removal without refund where permitted by law.</li>
    <li><strong>Privacy in the Community:</strong> Anything you post in the Community is visible to other members. Do not post personal financial information, account numbers, or anything you would not want made public. We may use anonymized Community discussion (no names or handles) in educational content.</li>
    <li><strong>Platform risk:</strong> Discord is a third-party platform. We are not responsible for Discord outages, data practices, or account actions taken by Discord itself.</li>
  </ul>

  <h2 id="conduct"><span class="num">Section 09</span>Acceptable Use &amp; Conduct</h2>
  <p>You agree not to: (a) use the Services for any unlawful purpose; (b) scrape, crawl, or bulk-download the Services by automated means except for legitimate search-engine indexing; (c) attempt to gain unauthorized access to our systems or other users' accounts; (d) misrepresent your identity or affiliation; (e) resell, sublicense, or commercially exploit the Services without written permission; or (f) interfere with the operation of the Services.</p>

  <h2 id="ip"><span class="num">Section 10</span>Intellectual Property</h2>
  <p>The Services — including the LA Traders name and lion mark, the RRR framework name and materials, the 6:00 AM Protocol materials, all text, graphics, templates, checklists, and design — are owned by LA Traders and protected by copyright, trademark, and other laws.</p>
  <p>With a purchase or free download, you receive a <strong>limited, non-exclusive, non-transferable license for personal use only</strong>. You may print the checklist for your own desk. You may not: republish, redistribute, resell, share your login or files, post paid materials publicly, or create derivative products for distribution. Sharing RRR OS Lite files or your Discord access is grounds for termination without refund.</p>

  <h2 id="thirdparty"><span class="num">Section 11</span>Third-Party Platforms &amp; Links</h2>
  <p>The Services run on or link to third-party platforms we do not control — including Discord, our email service provider, our SMS provider, payment processors (e.g., Stripe), and analytics tools. Your use of those platforms is governed by their own terms and privacy policies. We are not responsible for third-party content, policies, outages, or practices.</p>

  <h2 id="disclaimers"><span class="num">Section 12</span>Disclaimers &amp; Limitation of Liability</h2>
  <p><strong>THE SERVICES ARE PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED</strong>, including implied warranties of merchantability, fitness for a particular purpose, and non-infringement. We do not warrant that the Services will be uninterrupted, error-free, or that any content will produce any particular trading result.</p>
  <p><strong>TO THE MAXIMUM EXTENT PERMITTED BY LAW, LA TRADERS AND ITS OWNERS, OPERATORS, AND CONTRIBUTORS WILL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES — INCLUDING TRADING LOSSES, LOST PROFITS, OR LOST DATA — ARISING FROM OR RELATED TO YOUR USE OF THE SERVICES, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.</strong> Our total aggregate liability for any claim arising from the Services will not exceed the greater of (a) the amount you paid us in the 12 months before the claim or (b) $100.</p>

  <h2 id="indemnity"><span class="num">Section 13</span>Indemnification</h2>
  <p>You agree to indemnify and hold harmless LA Traders from any claims, damages, losses, and expenses (including reasonable attorneys' fees) arising from your use of the Services, your violation of these Terms, your trading activity, or your violation of any law or third-party rights.</p>

  <h2 id="termination"><span class="num">Section 14</span>Termination</h2>
  <p>You may stop using the Services at any time (unsubscribe from emails, reply STOP to texts, leave the Discord). We may suspend or terminate your access at any time for violation of these Terms or to protect the community, with or without notice. Sections that by their nature should survive (including 2, 3, 10, 12, 13, and 15) survive termination.</p>

  <h2 id="law"><span class="num">Section 15</span>Governing Law &amp; Disputes</h2>
  <p>These Terms are governed by the laws of the State of California, without regard to conflict-of-laws rules. Any dispute arising from the Services will be resolved in the state or federal courts located in Los Angeles County, California, and you consent to their jurisdiction, except that either party may bring an individual claim in small claims court.</p>

  <h2 id="changes"><span class="num">Section 16</span>Changes to These Terms</h2>
  <p>We may update these Terms from time to time. The "Last Updated" date at the top reflects the current version. Material changes will be announced via the site, email, or Discord. Continued use of the Services after changes take effect constitutes acceptance.</p>

  <h2 id="contact"><span class="num">Section 17</span>Contact</h2>
  <p>LA Traders &middot; Los Angeles, California<br>
  Email: <a href="mailto:support@latraderrrs.com">support@latraderrrs.com</a><br>
  Website: <a href="https://latraderrrs.com">latraderrrs.com</a></p>
</div>"""

PRIVACY_HTML = """<div class="wrap legal-body">
  <div class="crumb"><a href="/">Home</a> / Privacy Policy</div>
  <h1>Privacy <em>Policy</em></h1>
  <div class="legal-updated">Last Updated: __TODAY__ &middot; LA Traders &middot; Los Angeles, California</div>

  <div class="toc">
    <div class="toc-title">Contents</div>
    <ol>
      <li><a href="#overview">Overview</a></li>
      <li><a href="#collect">Information We Collect</a></li>
      <li><a href="#use">How We Use Information</a></li>
      <li><a href="#email">Email Marketing</a></li>
      <li><a href="#sms">SMS / Text Messaging Data</a></li>
      <li><a href="#discord">Discord Community Data</a></li>
      <li><a href="#cookies">Cookies &amp; Analytics</a></li>
      <li><a href="#sharing">How We Share Information</a></li>
      <li><a href="#retention">Data Retention</a></li>
      <li><a href="#security">Security</a></li>
      <li><a href="#rights">Your Rights &amp; Choices</a></li>
      <li><a href="#ccpa">California Residents (CCPA/CPRA)</a></li>
      <li><a href="#children">Children's Privacy</a></li>
      <li><a href="#international">International Users</a></li>
      <li><a href="#changes">Changes to This Policy</a></li>
      <li><a href="#contact">Contact</a></li>
    </ol>
  </div>

  <h2 id="overview"><span class="num">Section 01</span>Overview</h2>
  <p>This Privacy Policy explains what information LA Traders ("we," "us," "our") collects when you use latraderrrs.com, download the RRR Daily Trading Checklist, purchase RRR OS Lite, subscribe to our emails or SMS program, or join our Discord community — and how we use, share, and protect it. By using the Services, you agree to this Policy.</p>
  <div class="legal-note"><p>The short version: we collect the minimum needed to deliver what you asked for, we never sell your personal information, and every marketing channel has a one-step opt-out.</p></div>

  <h2 id="collect"><span class="num">Section 02</span>Information We Collect</h2>
  <p><strong>Information you give us directly:</strong></p>
  <ul>
    <li><strong>Email address</strong> — when you download the checklist, join the list, or make a purchase.</li>
    <li><strong>Name and billing details</strong> — when you purchase a product (payment card details are processed by our payment processor and never touch our servers).</li>
    <li><strong>Mobile phone number</strong> — only if you opt in to the SMS program.</li>
    <li><strong>Discord username/handle and anything you post</strong> — if you join the Community.</li>
    <li><strong>Support correspondence</strong> — when you email us.</li>
  </ul>
  <p><strong>Information collected automatically:</strong></p>
  <ul>
    <li><strong>Usage data</strong> — pages visited, time on page, referring links, and general device/browser information.</li>
    <li><strong>Cookies and similar technologies</strong> — see Section 7.</li>
    <li><strong>Approximate location</strong> — inferred from IP address at the region level (not precise GPS).</li>
  </ul>
  <p>We do <strong>not</strong> collect brokerage account data, trading account numbers, or government IDs.</p>

  <h2 id="use"><span class="num">Section 03</span>How We Use Information</h2>
  <ul>
    <li>Deliver the checklist, products, and community access you requested;</li>
    <li>Send transactional messages (receipts, delivery links, support responses);</li>
    <li>Send marketing emails and (if opted in) SMS messages, per your consent;</li>
    <li>Operate and moderate the Discord community;</li>
    <li>Understand what content is useful and improve the Services;</li>
    <li>Prevent abuse, fraud, and violations of our Terms;</li>
    <li>Comply with legal obligations.</li>
  </ul>

  <h2 id="email"><span class="num">Section 04</span>Email Marketing</h2>
  <p>When you subscribe, your email address and subscription source (e.g., "checklist download") are stored with our email service provider. We use this to send the content you asked for plus related educational and marketing emails.</p>
  <p><strong>Opt-out:</strong> Every marketing email contains a one-click unsubscribe link. Unsubscribing stops marketing emails promptly; transactional emails tied to an active purchase may continue as needed. We honor unsubscribes within 10 business days at the latest, consistent with the CAN-SPAM Act, and we never sell or rent email addresses to third parties for their own marketing.</p>

  <h2 id="sms"><span class="num">Section 05</span>SMS / Text Messaging Data</h2>
  <p>If you opt in to SMS, we collect your mobile number, opt-in timestamp and method, and message delivery status. This information is used solely to operate the SMS program — sending the messages you signed up for, honoring STOP/HELP requests, and maintaining proof of consent as required by the TCPA.</p>
  <ul>
    <li><strong>Opt-out:</strong> Reply <strong>STOP</strong> at any time. Opt-outs are honored immediately, and your number is suppressed from future sends (we retain the suppression record to respect your choice).</li>
    <li><strong>No sharing for third-party marketing:</strong> We do not sell, rent, or share your mobile number or SMS opt-in data with third parties or affiliates for their marketing purposes.</li>
    <li><strong>Service providers:</strong> Your number is processed by our SMS delivery provider solely to transmit messages on our behalf, under contract.</li>
  </ul>

  <h2 id="discord"><span class="num">Section 06</span>Discord Community Data</h2>
  <p>If you join our Discord server, we can see your Discord username, avatar, and anything you post in the server — that is how Discord works. We use this to moderate the community and grant role-based access (e.g., product-holder channels).</p>
  <ul>
    <li><strong>Public within the Community:</strong> Assume anything you post in the server is visible to other members. Do not share account numbers, addresses, or sensitive personal information.</li>
    <li><strong>Discord's own data practices</strong> are governed by Discord's Privacy Policy; we do not control and are not responsible for Discord's data handling.</li>
    <li><strong>Leaving:</strong> You can leave the server at any time. To request deletion of your moderation records with us, email <a href="mailto:privacy@latraderrrs.com">privacy@latraderrrs.com</a>.</li>
  </ul>

  <h2 id="cookies"><span class="num">Section 07</span>Cookies &amp; Analytics</h2>
  <p>We use a small set of cookies and similar technologies:</p>
  <ul>
    <li><strong>Essential:</strong> required for the site to function (e.g., remembering your session or preferences).</li>
    <li><strong>Analytics:</strong> to understand aggregate traffic (which pages are read, where visitors come from). We use privacy-respecting, aggregate analytics wherever practical.</li>
    <li><strong>Marketing attribution:</strong> to know which channel (search, social, email) brought you to us.</li>
  </ul>
  <p>You can block or delete cookies through your browser settings; the site will still function for reading content. We honor browser "Do Not Track" signals where technically feasible and do not respond to them with additional tracking.</p>

  <h2 id="sharing"><span class="num">Section 08</span>How We Share Information</h2>
  <p><strong>We never sell your personal information.</strong> We share it only in these cases:</p>
  <ul>
    <li><strong>Service providers (processors):</strong> our email platform, SMS delivery provider, payment processor, hosting provider, and analytics tools — each under contract and limited to providing their service to us.</li>
    <li><strong>Legal:</strong> if required by law, subpoena, or to protect the rights, safety, or property of LA Traders, our members, or the public.</li>
    <li><strong>Business transfer:</strong> if LA Traders is involved in a merger, acquisition, or asset sale, your information may transfer as part of that transaction, with this Policy continuing to apply.</li>
  </ul>

  <h2 id="retention"><span class="num">Section 09</span>Data Retention</h2>
  <p>We keep personal information only as long as needed: subscriber data while you remain subscribed; purchase records as required for tax and accounting (typically 7 years); SMS consent records as needed to demonstrate compliance; support correspondence for up to 24 months. When data is no longer needed, it is deleted or de-identified.</p>

  <h2 id="security"><span class="num">Section 10</span>Security</h2>
  <p>We use industry-standard measures: HTTPS everywhere, payment data handled exclusively by PCI-compliant processors, access to personal data limited to those who need it to operate the Services. No method of transmission or storage is 100% secure; if a breach affects your personal information, we will notify you as required by law.</p>

  <h2 id="rights"><span class="num">Section 11</span>Your Rights &amp; Choices</h2>
  <ul>
    <li><strong>Access &amp; correction:</strong> ask us what personal information we hold about you and request corrections.</li>
    <li><strong>Deletion:</strong> request deletion of your personal information, subject to legal retention requirements.</li>
    <li><strong>Opt-outs:</strong> unsubscribe links in every email; STOP for texts; leave the Discord anytime.</li>
    <li><strong>Cookie controls:</strong> via your browser settings.</li>
  </ul>
  <p>To exercise any of these, email <a href="mailto:privacy@latraderrrs.com">privacy@latraderrrs.com</a>. We respond within 30 days.</p>

  <h2 id="ccpa"><span class="num">Section 12</span>California Residents (CCPA/CPRA)</h2>
  <p>If you are a California resident, you have the right to: (a) know the categories and specific pieces of personal information we collect, use, and disclose; (b) request deletion of your personal information; (c) correct inaccurate information; (d) opt out of the sale or sharing of personal information — <strong>note that we do not sell or share personal information for cross-context behavioral advertising</strong>; and (e) not be discriminated against for exercising these rights. Submit requests to <a href="mailto:privacy@latraderrrs.com">privacy@latraderrrs.com</a>; we will verify your request before acting.</p>

  <h2 id="children"><span class="num">Section 13</span>Children's Privacy</h2>
  <p>The Services are not directed to children under 13 (or under 18 for purchases and community access), and we do not knowingly collect their personal information. If you believe a child has provided us information, contact us and we will delete it.</p>

  <h2 id="international"><span class="num">Section 14</span>International Users</h2>
  <p>The Services are operated from the United States. If you access them from elsewhere, you understand your information will be processed in the US, where data protection laws may differ from yours. Where GDPR applies, our legal bases for processing are: performance of a contract (delivering what you bought or requested), consent (marketing emails and SMS — withdrawable anytime), and legitimate interest (operating and improving the Services).</p>

  <h2 id="changes"><span class="num">Section 15</span>Changes to This Policy</h2>
  <p>We may update this Policy as the Services evolve. The "Last Updated" date reflects the current version; material changes will be announced via the site or email. Continued use after changes take effect constitutes acceptance.</p>

  <h2 id="contact"><span class="num">Section 16</span>Contact</h2>
  <p>LA Traders &middot; Los Angeles, California<br>
  Privacy requests: <a href="mailto:privacy@latraderrrs.com">privacy@latraderrrs.com</a><br>
  General support: <a href="mailto:support@latraderrrs.com">support@latraderrrs.com</a></p>
</div>"""

def build_legal_page(slug, title, desc, body_html):
    canonical = f"{BASE}/{slug}/"
    body_html = body_html.replace("__TODAY__", TODAY)
    schema = ldjson({
        "@context": "https://schema.org", "@type": "WebPage",
        "name": title, "description": desc, "url": canonical,
        "isPartOf": {"@type": "WebSite", "name": "LA Traders", "url": BASE + "/"},
    })
    return head(title, desc, canonical, schema, LEGAL_CSS) + body_html + foot()

os.makedirs(os.path.join(OUT, "terms"), exist_ok=True)
os.makedirs(os.path.join(OUT, "privacy"), exist_ok=True)

with open(os.path.join(OUT, "terms", "index.html"), "w") as f:
    f.write(build_legal_page("terms", "Terms of Service — LA Traders",
        "Terms of Service for LA Traders: educational content disclaimer, risk disclosure, email marketing, SMS text program, Discord community rules, billing, and intellectual property.",
        TERMS_HTML))
print("Built /terms/")

with open(os.path.join(OUT, "privacy", "index.html"), "w") as f:
    f.write(build_legal_page("privacy", "Privacy Policy — LA Traders",
        "Privacy Policy for LA Traders: what we collect, email marketing (CAN-SPAM), SMS data (TCPA), Discord community data, cookies, your rights, and CCPA/CPRA disclosures.",
        PRIVACY_HTML))
print("Built /privacy/")
