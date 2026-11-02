const dlg = document.getElementById('checkout');
  const CHECKOUT_URL = 'https://bookmoths.lemonsqueezy.com/checkout/buy/db743329-9fbc-4657-ba57-2a8d8b5bd05d?media=0&discount=0';
  document.querySelectorAll('.buy').forEach(x => x.addEventListener('click', () => CHECKOUT_URL ? (location.href = CHECKOUT_URL) : dlg.showModal()));
  document.getElementById('close-checkout').addEventListener('click', () => dlg.close());
  const mainBuy = document.querySelector('.buyrow');
  if (mainBuy && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => document.body.classList.toggle('past-buy', !en.isIntersecting && en.boundingClientRect.top < 0)).observe(mainBuy);
  } else { document.body.classList.add('past-buy'); }
