# Generates one page per book from src/site/books.json.
# Run from build_deploy.py (uses its OUT, SRC, EMAIL, CHECKOUTS, page, og, externalize).
import json as _json, html as _html

BOOKS = _json.loads((SRC / 'books.json').read_text())
_NUMW = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()


def _numw(n):
    if n <= 20:
        return _NUMW[n]
    return 'twenty-' + _NUMW[n - 20] if n < 30 else str(n)


_CHECK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10l4 4 8-9"/></svg>'


def _plural(n, word):
    return f'{n} {word}' + ('s' if n != 1 else '')


def book_main(b):
    e = _html.escape
    nparts, nch, nws = len(b['parts']), len(b['chapters']), len(b['worksheets'])
    parts = ''.join(
        f'<div class="part"><div class="n">{i + 1:02d}</div><h3>{e(p["name"])}</h3><p>{e(t)}</p></div>'
        for i, (p, t) in enumerate(zip(b['parts'], b['blurbs'])))
    toc = ''.join(f'<li>{e(c)}</li>' for c in b['chapters'])
    ws = b['worksheets'][-1] if nws == 1 else ', '.join(b['worksheets'][:-1]) + ' and ' + b['worksheets'][-1]
    smp = b['sample']
    paras = ''.join(('<p class="first">' if i == 0 else '<p>') + p + '</p>' for i, p in enumerate(smp['paras']))
    price = f"${b['price']}"
    faq = [
        ('What exactly will I get?', f"A {b['pages']}-page PDF eBook with {nch} chapters and {_plural(nws, 'worksheet')} you can print or fill in on paper."),
        ('How do I receive it?', "Right after you pay, you'll see a download link, and a copy goes to your email. Nothing to wait for, nothing shipped."),
        ('Can I read it on my phone or Kindle?', 'Yes. A PDF opens on any phone, tablet or computer, and you can send it to the Kindle app.'),
        ('Can I print the worksheets?', 'Yes, as many times as you like for your own use.'),
        ('Can I get a refund?', "Because this is a digital download you get instantly, all sales are final. If your file doesn't arrive or won't open, email us and we'll fix it or send it again right away. If you were charged twice by mistake, we'll refund the extra payment."),
        tuple(b['faq_extra']),
    ]
    faqh = ''.join(f'<details><summary>{e(q)}</summary><div class="in">{e(a)}</div></details>' for q, a in faq)
    checkout = CHECKOUTS.get(b['slug'], '')
    return f'''<main>
  <section class="product" style="padding:0">
    <div class="wrap" style="display:block;padding:0 max(20px,env(safe-area-inset-right,0px)) 0 max(20px,env(safe-area-inset-left,0px))">
      <div class="crumbs" style="position:relative;z-index:1"><a href="/#catalog">Books</a> / {e(b['title'])}</div>
    </div>
    <div class="wrap">
      <div class="art"><img class="book3d" src="/img/bk-{b['img']}.webp" alt="{e(b['alt'])}" width="{b['w']}" height="900"></div>
      <div class="copy">
        <h1>{e(b['title'])}</h1>
        <p class="sub">{e(b['sub'])}</p>
        <p class="pitch">{e(b['pitch'])}</p>
        <div class="buyrow">
          <span class="pricebox"><span class="price">{price}</span></span>
          <button class="btn buy" type="button">Get the eBook</button>
          <a href="#sample" style="color:var(--link);font-weight:600;font-size:15px;text-decoration:none">Read a sample &rarr;</a>
        </div>
        <ul class="assure">
          <li>{_CHECK}Instant PDF download, plus a copy to your email</li>
          <li>{_CHECK}{b['pages']} pages &middot; {nch} chapters &middot; {_plural(nws, 'worksheet')}</li>
          <li>{_CHECK}Secure checkout: card, PayPal, Apple Pay</li>
        </ul>
      </div>
    </div>
  </section>

  <nav class="pagenav" aria-label="On this page">
    <div class="wrap">
      <div class="tabs"><a href="#inside">Inside</a><a href="#sample">Sample</a><a href="#faq">FAQ</a></div>
      <div class="mini-buy"><span class="price">{price}</span><button class="btn sm buy" type="button">Get the eBook</button></div>
    </div>
  </nav>

  <section id="inside" style="padding-top:16px">
    <div class="wrap">
      <div class="head"><h2>{_numw(nparts).capitalize()} parts. {_numw(nch).capitalize()} chapters.</h2></div>
      <div class="parts">{parts}</div>
      <details class="all">
        <summary>See all {nch} chapters and {_plural(nws, 'worksheet')}</summary>
        <div class="in">
          <ol class="toc">{toc}</ol>
          <p style="margin:16px 0 0" class="muted">Worksheets: {e(ws)}.</p>
        </div>
      </details>
    </div>
  </section>

  <section id="sample">
    <div class="wrap excerpt">
      <div>
        <h2 style="margin:10px 0 14px">A page from Chapter {smp['n']}</h2>
        <p class="muted">Short chapters in plain English, most ending with something to try. Here's how one begins.</p>
        <button class="btn ghost buy" type="button">Get the whole book</button>
      </div>
      <article class="page">
        <div class="cn">{smp['n']}</div>
        <h4>{e(smp['title'])}</h4>
        {paras}
        <div class="pn">{smp['page'] or ''}</div>
      </article>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <div class="head" style="margin-bottom:12px"><h2>Good to know</h2></div>
      <div class="faq">{faqh}</div>
    </div>
  </section>
</main>

<div class="buybar">
  <div><b>{e(b['title'])}</b><span>{price} &middot; instant PDF</span></div>
  <button class="btn sm buy" type="button">Get the eBook</button>
</div>

<dialog id="checkout">
  <h3>Checkout opens very soon</h3>
  <p style="margin-top:10px">This book is ready and checkout is being set up right now. Please check back in a day or two, or write to <a href="mailto:{EMAIL}" style="color:var(--link)">{EMAIL}</a> and we'll email you the moment it's live.</p>
  <button class="btn" type="button" id="close-checkout">Got it</button>
</dialog>

<script>
  const dlg = document.getElementById('checkout');
  const CHECKOUT_URL = '{checkout}';
  document.querySelectorAll('.buy').forEach(x => x.addEventListener('click', () => CHECKOUT_URL ? (location.href = CHECKOUT_URL) : dlg.showModal()));
  document.getElementById('close-checkout').addEventListener('click', () => dlg.close());
  const mainBuy = document.querySelector('.buyrow');
  if (mainBuy && 'IntersectionObserver' in window) {{
    new IntersectionObserver(([en]) => document.body.classList.toggle('past-buy', !en.isIntersecting && en.boundingClientRect.top < 0)).observe(mainBuy);
  }} else {{ document.body.classList.add('past-buy'); }}
</script>'''


for b in BOOKS:
    from PIL import Image as _Img
    b['w'] = _Img.open(SRC / 'img' / f"bk-{b['img']}.webp").width
    d = b['pitch'] if len(b['pitch']) <= 158 else b['pitch'][:155].rsplit(' ', 1)[0] + '…'
    (OUT / f"{b['slug']}.html").write_text(page(
        f"{b['title']} · Bookmoth", _html.escape(d),
        externalize(book_main(b), 'book-' + b['slug']),
        og(_html.escape(b['title'] + ': ' + b['sub']), _html.escape(d), f"og-{b['slug']}.jpg", '/' + b['slug']),
        'has-buybar'))
