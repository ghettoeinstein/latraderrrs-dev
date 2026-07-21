# PRD: LA Traders — Glossary SEO Moat & Static Interactive Tools

**Product:** latraderrrs.com
**Stack constraint:** Fully static, GitHub-hosted. No servers, no databases, no AI/LLM calls at runtime. Vanilla JS + localStorage only.

## 1. Problem Statement

Glossary pages are shallow and isolated — no cross-linking, no tie-back to the 6:00 AM Protocol. This caps SEO compounding and fails to brand the terminology as LA Traders' own system.

Only interactive asset is a static PDF — no reason to return daily. No calculator, no journal, no habit loop.

## 2. Goals

- Turn the glossary into a self-reinforcing SEO moat.
- Make "RRR Framework" / "6:00 AM Protocol" read as owned category language, not generic ICT jargon.
- Convert the checklist into a recurring-use tool.
- Ship a calculator that captures independent search traffic.
- Zero backend, all static.

## 3. Non-Goals

No AI/LLM features. No server logic, accounts, or DB. No pricing/gating changes this phase.

---

## Feature 1: Glossary Cross-Linking

- Each term gets a `related_terms` array (e.g. Reveal → Retrace, Run, RRR Framework, Liquidity Sweep), rendered as a "Related Terms" block.
- Bidirectional linking — no orphaned one-way links.
- Category pages (Market Structure, Liquidity, etc.) get real one-line definitions per child term, not bare link lists.
- Resubmit sitemap.xml after restructuring.
- **Metrics:** avg internal links/page (target 4–6), organic sessions to /glossary/*, pages/session site-wide.

## Feature 2: "How This Fits the 6:00 AM Protocol" Callout

- Static color-coded callout box (matching Blue/Purple/Red/White/Gold) on every glossary page tying the term to a Protocol stage or RRR step.
- Written once at build time, not generated — 1–2 sentences per term.
- Terms with no natural fit (Margin, Tick Value) get a lighter risk/execution-philosophy tie-in for consistency.
- **Metrics:** 100% glossary coverage at launch.

## Feature 3: Interactive RRR Daily Checklist (Web App)

- In-browser version of the PDF: checkboxes per Protocol stage, localStorage persistence keyed by date, streak counter.
- Resets daily; streak breaks if a day is missed.
- No accounts, no cross-device sync (explicit v1 scope).
- Graceful degrade if localStorage unavailable (private browsing).
- Subtle OS Lite ($17) upsell on completion.
- **Metrics:** return visits, % interacting with checkboxes, CTR to OS Lite.

## Feature 4: Position Size / Risk Calculator

- Inputs: account size, risk %, stop distance, instrument (preset ES/NQ tick values + manual entry).
- Outputs: max $ risk, recommended size, $/tick.
- Own indexable URL (`/tools/position-size-calculator/`) targeting "futures position size calculator" SEO.
- Ties back to RRR branding in on-page copy.
- **Metrics:** organic rankings, bounce rate, CTR to checklist/OS Lite.

## Feature 5: Downloadable Trade Journal Spreadsheet

- Google Sheets/Excel template, RRR-aligned columns (Reveal/Retrace/Run, R:R planned vs actual, etc.), built-in win-rate/expectancy/equity-curve formulas.
- Gated behind existing email-capture form (no new backend).
- **Metrics:** conversion rate, list growth vs. checklist baseline.

## Feature 6: Static Session Clock Widget

- Global header/footer widget counting down to next Protocol stage in NY time (client-side conversion, no server).
- Color-coded states matching the Protocol.
- **Metrics:** indirect — time-on-site, repeat visits across all pages.

---

## Phasing

| Phase | Feature | Effort |
|-------|---------|--------|
| 1 | Glossary cross-linking + Protocol callouts | Low |
| 2 | Position size calculator | Low-Med |
| 2 | Interactive checklist app | Med |
| 3 | Session clock widget | Low |
| 3 | Journal spreadsheet | Low |

## Risks

- localStorage-only persistence = no cross-device sync; don't overpromise in copy.
- Glossary restructuring touches every page — do as one batch, check for broken links, resubmit sitemap.
- Risk disclosure language must stay visible on all new tool pages.

## Open Questions

1. Dedicated /tools/ section vs. inline embeds?
2. Journal spreadsheet: free email-gate, or bundled into OS Lite at same $17 price?
