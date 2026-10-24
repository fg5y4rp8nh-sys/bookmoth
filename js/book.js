const dlg = document.getElementById('checkout');
  const CHECKOUT_URL = '';
  document.querySelectorAll('.buy').forEach(b => b.addEventListener('click', () => CHECKOUT_URL ? (location.href = CHECKOUT_URL) : dlg.showModal()));
  document.getElementById('close-checkout').addEventListener('click', () => dlg.close());
  const mainBuy = document.querySelector('.buyrow');
  if (mainBuy && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => document.body.classList.toggle('past-buy', !e.isIntersecting && e.boundingClientRect.top < 0)).observe(mainBuy);
  } else { document.body.classList.add('past-buy'); }
