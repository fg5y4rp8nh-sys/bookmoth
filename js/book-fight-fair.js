const dlg = document.getElementById('checkout');
  const CHECKOUT_URL = 'https://bookmoths.lemonsqueezy.com/checkout/buy/0d2718b8-0e92-409f-b08f-0e5dc4843a98?media=0&discount=0';
  document.querySelectorAll('.buy').forEach(x => x.addEventListener('click', () => CHECKOUT_URL ? (location.href = CHECKOUT_URL) : dlg.showModal()));
  document.getElementById('close-checkout').addEventListener('click', () => dlg.close());
  const mainBuy = document.querySelector('.buyrow');
  if (mainBuy && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => document.body.classList.toggle('past-buy', !en.isIntersecting && en.boundingClientRect.top < 0)).observe(mainBuy);
  } else { document.body.classList.add('past-buy'); }
