const dlg = document.getElementById('checkout');
  const CHECKOUT_URL = 'https://bookmoths.lemonsqueezy.com/checkout/buy/94b6d042-7310-4144-9538-e900de05ac3f?media=0&discount=0';
  document.querySelectorAll('.buy').forEach(x => x.addEventListener('click', () => CHECKOUT_URL ? (location.href = CHECKOUT_URL) : dlg.showModal()));
  document.getElementById('close-checkout').addEventListener('click', () => dlg.close());
  const mainBuy = document.querySelector('.buyrow');
  if (mainBuy && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => document.body.classList.toggle('past-buy', !en.isIntersecting && en.boundingClientRect.top < 0)).observe(mainBuy);
  } else { document.body.classList.add('past-buy'); }
