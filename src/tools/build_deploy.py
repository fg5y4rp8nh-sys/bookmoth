import re, shutil, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent   # repo/src
SRC = ROOT / 'site'
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/bookmoth-dist').resolve()  # build here, then copy to repo root
EMAIL = 'products000001@gmail.com'
SITE = 'https://bookmoth-ten.vercel.app'
CHECKOUT_URL = 'https://bookmoths.lemonsqueezy.com/checkout/buy/11bbae8e-f0db-4797-9f1b-cd2b07cc631b?media=0&discount=0'
if OUT.exists(): shutil.rmtree(OUT)
(OUT / 'img').mkdir(parents=True)
shutil.copy(SRC / 'cover.jpg', OUT / 'cover.jpg')
FONTS_DIR = ROOT / 'fonts'
(OUT / 'fonts').mkdir()
faces = []
for fam, pkg, prefix, variants in [
    ('Playfair Display', 'fontsource-playfair-display-5.1.0', 'playfair-display', [(500,'italic'),(600,'normal'),(600,'italic'),(700,'normal'),(800,'normal')]),
    ('DM Sans', 'fontsource-dm-sans-5.1.0', 'dm-sans', [(400,'normal'),(500,'normal'),(600,'normal'),(700,'normal')])]:
    for w, st in variants:
        fn = f'{prefix}-latin-{w}-{st}.woff2'
        shutil.copy(FONTS_DIR / fn, OUT / 'fonts' / fn)
        faces.append(f'@font-face {{ font-family: "{fam}"; font-style: {st}; font-weight: {w}; font-display: swap; src: url("/fonts/{fn}") format("woff2"); }}')
(OUT / 'styles.css').write_text('\n'.join(faces) + '\n' + (SRC / 'styles.css').read_text())
(OUT / 'js').mkdir()
for f in (SRC / 'img').iterdir(): shutil.copy(f, OUT / 'img' / f.name)

FONTS = '<link rel="preload" href="/fonts/playfair-display-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>'
HEADER = '''<header class="top">
  <div class="wrap">
    <a class="logo" href="/"><img class="logoimg" src="/img/logo-sm.png" alt="" width="48" height="31"><span class="word">Bookmoth</span></a>
    <nav aria-label="Main"><a href="/#catalog">Books</a><a href="/contact">Contact</a></nav>
  </div>
</header>'''
FOOTER = '''<footer class="sitefoot">
  <div class="wrap">
    <div><a class="logo" href="/" style="margin:0 0 12px"><img class="logoimg" src="/img/logo-sm.png" alt="" width="48" height="31"><span class="word">Bookmoth</span></a></div>
    <div><h5>Books</h5><a href="/retired-husband-syndrome">Retired Husband Syndrome</a><a href="/#catalog">Coming soon</a></div>
    <div><h5>Help</h5><a href="/contact">Contact</a><a href="/refund">Refund policy</a></div>
    <div><h5>Legal</h5><a href="/privacy">Privacy policy</a><a href="/terms">Terms of service</a><span class="small">© 2026 Bookmoth</span></div>
  </div>
</footer>'''

SCRIPT_N = [0]
def externalize(body, name):
    def rep(m):
        (OUT / 'js' / f'{name}.js').write_text(m.group(1).strip() + '\n')
        return f'<script src="/js/{name}.js" defer></script>'
    return re.sub(r'<script>(.*?)</script>', rep, body, flags=re.S)

def page(title, desc, body, extra_head='', body_cls=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/img/favicon.png">
{FONTS}
<link rel="stylesheet" href="/styles.css">
{extra_head}
</head>
<body{' class="'+body_cls+'"' if body_cls else ''}>
{HEADER}
{body}
{FOOTER}
</body>
</html>
'''

def og(title, desc, img, path='/'):
    return f'''<link rel="canonical" href="{SITE}{path}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:site_name" content="Bookmoth">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/img/{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">'''

def main_of(html):
    return html[html.index('<main>'):html.index('</main>') + 7]

def fix(html):
    html = re.sub(r'(src|href)="(img/|cover)', lambda m: f'{m.group(1)}="/{m.group(2)}', html)
    html = html.replace('href="book.html', 'href="/retired-husband-syndrome').replace('href="index.html', 'href="/')
    return html

# ---- home
idx = (SRC / 'index.html').read_text()
home_main = fix(main_of(idx))
home_main = re.sub(r'<form id="signup">.*?</form>', f'''<form id="signup" action="https://formsubmit.co/{EMAIL}" method="POST">
          <input type="hidden" name="_subject" value="New Bookmoth subscriber">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
          <label for="email" style="position:absolute;left:-9999px">Email address</label>
          <input id="email" type="email" name="email" required placeholder="Your email" autocomplete="email">
          <button class="btn sm" type="submit">Notify me</button>
        </form>
        <dialog id="consent" aria-labelledby="consent-t">
          <h3 id="consent-t">Before we add you</h3>
          <p style="margin:12px 0 0">We'll only email you when a new Bookmoth book is out. No spam, and you can unsubscribe anytime. Your email is handled as described in our <a href="/privacy" style="color:var(--link)">Privacy policy</a>.</p>
          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px">
            <button class="btn" type="button" id="consent-ok">Agree &amp; subscribe</button>
            <button class="btn ghost" type="button" id="consent-no">Cancel</button>
          </div>
        </dialog>''', home_main, flags=re.S)
home_main = home_main.replace('<p>Get an email when the next one is out.</p>', '<p id="joinmsg">Get an email when the next one is out.</p>')
home_main = home_main.replace('href="#join"', 'href="#join"')
script = idx[idx.index('<script>'):idx.index('</script>') + 9]
script = re.sub(r"\s*document\.getElementById\('signup'\).*?\n", '\n', script)
script = script.replace('</script>', """  const sf = document.getElementById('signup'), dlg = document.getElementById('consent');
  async function send() {
    const btn = sf.querySelector('button'), msg = document.getElementById('joinmsg');
    btn.disabled = true; btn.textContent = 'Sending…';
    try {
      const r = await fetch('https://formsubmit.co/ajax/""" + EMAIL + """', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(Object.assign(Object.fromEntries(new FormData(sf)), { consent: 'Agreed to Privacy policy' })) });
      if (!r.ok) throw 0;
      msg.textContent = 'You’re on the list. Thank you!'; sf.reset(); btn.textContent = 'Done ✓';
    } catch (err) { btn.disabled = false; btn.textContent = 'Notify me'; msg.textContent = 'Something went wrong. Please try again.'; }
  }
  if (sf && dlg) {
    sf.addEventListener('submit', (e) => { e.preventDefault(); dlg.showModal(); });
    document.getElementById('consent-ok').addEventListener('click', () => { dlg.close(); send(); });
    document.getElementById('consent-no').addEventListener('click', () => dlg.close());
  }
</script>""")
home_desc = 'Bookmoth is an online bookstore of short, practical books on marriage, family, money and life’s big changes.'
(OUT / 'index.html').write_text(page('Bookmoth · Online bookstore', home_desc, externalize(home_main + '\n' + script, 'home'), og('Bookmoth · Online bookstore', home_desc, 'og-home.jpg')))

# ---- book page
bk = (SRC / 'book.html').read_text()
bk_main = fix(main_of(bk))
tail = bk[bk.index('</footer>') + 9:bk.index('</body>')]
tail = fix(tail)
tail = tail.replace("document.querySelectorAll('.buy').forEach(b => b.addEventListener('click', () => dlg.showModal()));",
  f"const CHECKOUT_URL = '{CHECKOUT_URL}';\n  document.querySelectorAll('.buy').forEach(b => b.addEventListener('click', () => CHECKOUT_URL ? (location.href = CHECKOUT_URL) : dlg.showModal()));")
tail = tail.replace('On the live site this button opens', 'Checkout opens soon. This button will open')
bdesc = "He's home all day now. A warm, practical guide to getting your space back without losing your marriage. 40 short chapters, 6 worksheets, instant PDF."
(OUT / 'retired-husband-syndrome.html').write_text(page('Retired Husband Syndrome · Bookmoth', bdesc, externalize(bk_main + tail, 'book'),
    og('Retired Husband Syndrome: And 40 Ways to Survive It With Your Marriage Intact', bdesc, 'og-rhs.jpg', '/retired-husband-syndrome'), 'has-buybar'))

# ---- legal pages
def legal(slug, title, intro, sections):
    secs = ''.join(f'<h2 style="font-size:24px;margin:34px 0 10px">{h}</h2>' + ''.join(f'<p>{p}</p>' for p in ps) for h, ps in sections)
    body = f'''<main>
  <section>
    <div class="wrap" style="max-width:760px">
      <h1 style="font-size:clamp(36px,5vw,52px)">{title}</h1>
      <p class="small" style="margin-top:10px">Last updated: October 25, 2026</p>
      <p class="muted" style="font-size:18px;margin-top:20px">{intro}</p>
      {secs}
    </div>
  </section>
</main>'''
    (OUT / f'{slug}.html').write_text(page(f'{title} · Bookmoth', f'{title} for Bookmoth.', body))

M = f'<a href="mailto:{EMAIL}" style="color:var(--link)">{EMAIL}</a>'
legal('contact', 'Contact', 'Questions about an order or a download link that didn’t arrive? Write to us and a real person will answer, usually within two business days.', [
  ('Email', [f'{M}']),
  ('Order problems', ['Please include the email address you used at checkout and your order number from the receipt. That lets us find your order right away.']),
  ('Didn’t get your download?', ['Check your spam or promotions folder for an email from Lemon Squeezy, our payment provider. If it isn’t there, email us and we’ll resend your link.']),
])
legal('refund', 'Refund policy', 'Our books are digital downloads delivered instantly, so all sales are final. Here’s what we will always do for you.', [
  ('All sales are final', ['Because you get immediate access to the full book as soon as you pay, we don’t offer refunds if you change your mind or the book isn’t what you expected. Please read the description, table of contents and free sample on the book page before buying.']),
  ('If something goes wrong', [f'If your download link doesn’t arrive, the file won’t open, or it’s damaged, email {M} and we’ll fix it or send you a working copy right away.', 'If you were accidentally charged twice for the same book, we’ll refund the duplicate payment.']),
  ('How payments are handled', ['Payments are processed by Lemon Squeezy, our reseller and Merchant of Record. Any approved refund goes back to the original payment method.']),
])
legal('privacy', 'Privacy policy', 'This page explains what information Bookmoth collects, why, and what you can do about it. The short version: we collect as little as possible and never sell it.', [
  ('Purchases', ['Orders are processed by Lemon Squeezy, which acts as the Merchant of Record. Lemon Squeezy collects your name, email address, billing country and payment details to complete the sale, deliver your download and handle taxes. We never see or store your full card details. Lemon Squeezy’s own privacy policy applies to that information.', 'From Lemon Squeezy we receive your name, email address, what you bought and when. We use it only to deliver your purchase, answer support requests and process refunds.']),
  ('Emails', [f'If you write to us or ask to be notified about new books, we keep your email address to reply or send that notice. We don’t send daily newsletters, and you can ask us to remove your address at any time by writing to {M}.']),
  ('Cookies and analytics', ['This website does not set cookies and does not use analytics or advertising trackers. Fonts are hosted on our own site, so no third-party font service sees your visit. The checkout page, run by Lemon Squeezy, may use cookies needed to complete your payment.']),
  ('Service providers', ['We use a small number of providers to run this site: Vercel (website hosting, which keeps basic technical logs such as IP address and browser type for security), FormSubmit (delivers the “notify me” form to our inbox) and Lemon Squeezy (checkout, payments and file delivery). They process data only to provide these services.']),
  ('Children', ['Our books and this website are intended for adults. We do not knowingly collect information from children under 16.']),
  ('Your rights', [f'You can ask us what information we hold about you, ask us to correct it, or ask us to delete it. Email {M} and we’ll respond within 30 days.']),
  ('Changes', ['If we change this policy, we’ll update the date at the top of this page.']),
])
legal('terms', 'Terms of service', 'By buying from or using Bookmoth, you agree to these terms. They’re written to be read, so please do.', [
  ('Who sells the books', ['Bookmoth books are sold through Lemon Squeezy, our online reseller and Merchant of Record. Lemon Squeezy handles payment, invoicing and sales tax, and its terms of sale also apply to your purchase.']),
  ('What you’re buying', ['Our books are digital products delivered as PDF files. After payment you get a download link right away and a copy by email. Nothing is shipped.']),
  ('Your license', ['When you buy a book, you get a personal, non-transferable license to read it and to print copies of its worksheets for your own household. Please don’t resell, share, upload or redistribute the files. Each book is protected by copyright.']),
  ('Not professional advice', ['Our books are for general information and education. They are not a substitute for medical, psychological, legal or financial advice. If you or someone you know is in crisis or in danger, contact local emergency services.']),
  ('Refunds', ['See our <a href="/refund" style="color:var(--link)">refund policy</a>. In short: all sales are final, but if your file doesn’t arrive or doesn’t work, we’ll make it right.']),
  ('Contact', [f'Questions about these terms: {M}.']),
])

import json
CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://formsubmit.co; form-action 'self' https://formsubmit.co mailto:; frame-ancestors 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests"
(OUT / 'vercel.json').write_text(json.dumps({
  "cleanUrls": True, "trailingSlash": False,
  "headers": [{"source": "/(.*)", "headers": [
    {"key": "Content-Security-Policy", "value": CSP},
    {"key": "X-Content-Type-Options", "value": "nosniff"},
    {"key": "X-Frame-Options", "value": "DENY"},
    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
    {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=()"},
    {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains"}]}]
}, indent=2) + '\n')
(OUT / 'README.md').write_text('# Bookmoth\n\nStatic bookstore site. Deployed on Vercel.\n\n- `index.html` – home and catalog\n- `retired-husband-syndrome.html` – book page (set `CHECKOUT_URL` in the script at the bottom)\n- `privacy.html`, `terms.html`, `refund.html`, `contact.html` – legal pages\n')
print(sorted(p.name for p in OUT.iterdir()))

# ---- link preview images
from PIL import Image, ImageDraw
for src, out in [('hero.webp', 'og-home.jpg'), ('book3d.webp', 'og-rhs.jpg')]:
    c = Image.new('RGB', (1200, 630), (248, 227, 225)); d = ImageDraw.Draw(c)
    d.ellipse((820, -180, 1380, 300), fill=(247, 231, 184)); d.ellipse((-160, 420, 300, 820), fill=(211, 232, 225))
    im = Image.open(OUT / 'img' / src).convert('RGBA'); im.thumbnail((2000, 590), Image.LANCZOS)
    c.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2), im); c.save(OUT / 'img' / out, quality=88)

(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
urls = ['/', '/retired-husband-syndrome', '/contact', '/refund', '/privacy', '/terms']
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{u if u != "/" else ""}</loc></url>\n' for u in urls) + '</urlset>\n')
