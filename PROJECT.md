# Bookmoth — project notes (read this first in a new chat)

Online bookstore of short practical eBooks for an English-speaking (mainly US) audience.
Owner lives in Vietnam. Sales go through Lemon Squeezy (approved, live).

## Live
- Site: https://bookmoth-ten.vercel.app (Vercel, auto-deploys from `main` of this repo)
- Book page / link for socials: https://bookmoth-ten.vercel.app/retired-husband-syndrome
- Checkout (live): https://bookmoths.lemonsqueezy.com/checkout/buy/11bbae8e-f0db-4797-9f1b-cd2b07cc631b?media=0&discount=0
- Contact / support email: products000001@gmail.com
- Email signup: FormSubmit (AJAX) → owner's inbox, with a privacy-consent popup.

## Repo layout
- Root = the built static site that Vercel serves (`index.html`, `retired-husband-syndrome.html`, legal pages, `styles.css`, `js/`, `img/`, `fonts/`, `vercel.json` with security headers + CSP).
- `src/site/` = editable sources (`index.html` home, `book.html` book page, `styles.css`, images).
- `src/tools/build_deploy.py` = builds the site: self-hosted fonts, external JS, legal pages, OG images, sitemap, CSP. Settings at the top: `EMAIL`, `SITE`, `CHECKOUT_URL`.
- `src/fonts/` = woff2 fonts (Playfair Display, DM Sans).
- `src/tools/serve.py` = local preview server with clean URLs + headers; `crawl.js` = Playwright link/overflow checker.
- `src/` and this file are excluded from deployment by `.vercelignore`.

## How to change the site
1. Edit files in `src/site/` (or settings in `build_deploy.py`).
2. `python3 src/tools/build_deploy.py /tmp/dist`
3. Copy `/tmp/dist/*` over the repo root (keep `.git`, `src/`, `PROJECT.md`, `.vercelignore`, `README.md`), commit, push → Vercel deploys in ~1 min.
4. Optional check: `python3 src/tools/serve.py /tmp/dist` (port 4175) and `node src/tools/crawl.js`.

## Brand & design decisions
- Name: Bookmoth. Logo = moth whose wings are book pages (img/logo*.png). Animated wordmark: letters rise, the moth hatches from the "o" and loops around before landing on the "h".
- Hero tagline: “Just one more chapter, then sleep.” Famous last words.
- Palette: blush #F8E3E1, butter, mint, terracotta accent #C2512E; Playfair Display + DM Sans.
- No decorative blobs on the book page (owner disliked them); soft "lamp-glow" backdrops instead.
- Catalog shows 3D book mockups (img/book3d*, b-quiet, b-parents, b-60).

## Books
- Out now: "Retired Husband Syndrome: And 40 Ways to Survive It With Your Marriage Intact" — 74-page PDF, 40 chapters, 6 worksheets. The PDF and manuscript are NOT in this public repo (paid product); the owner keeps them in the project zip.
- Coming soon (covers only): The Quiet House, Caring for Mom & Dad, Before You Turn 60.

## Pricing & policies
- Launch price $25, regular $45 — launch ends Nov 30 2026 (must really raise the price or move the date; no fake discounts).
- Refunds: all sales final; resend/fix broken or missing files; refund duplicate charges.
- Lemon Squeezy is Merchant of Record (taxes). Payouts to a Vietnamese bank, 1st/15th, 13-day hold, $50 minimum.

## Rules the owner and I agreed on
- No fabricated reviews, stats, "true story" claims or fake credentials.
- Owner wants concise answers in Russian; hates generic "AI-looking" text and design.
- Threads: manual posting only, 3–4 branches/day, 2–3 h apart; English account for Bookmoth.

## Next ideas
- Separate English Threads/Instagram account for Bookmoth; animated story Reels (separate project) end with "More stories like this on my profile".
- Move the email list to MailerLite or Lemon Squeezy email later.
- Each new book: same page template, own URL, 3D cover, Lemon Squeezy product + checkout link.
