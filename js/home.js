const cards = [...document.querySelectorAll('#books .bk')], none = document.getElementById('noresult'), chips = [...document.querySelectorAll('.chip')];
  let topic = '';
  function apply() {
    let n = 0;
    cards.forEach(c => { const ok = (!topic || c.dataset.t === topic) ; c.style.display = ok ? '' : 'none'; n += ok; });
    none.hidden = n > 0;
  }
  chips.forEach(ch => ch.addEventListener('click', () => { topic = ch.dataset.f; chips.forEach(x => x.setAttribute('aria-pressed', x === ch)); apply(); }));
  (function(){
    const h1=document.querySelector('.brandword'); if(!h1) return;
    const m=h1.querySelector('.moth'), t=h1.querySelectorAll('.l')[7];
    setTimeout(()=>{ const a=m.getBoundingClientRect(), b=t.getBoundingClientRect();
      h1.style.setProperty('--dx',(b.left+b.width*0.55-(a.left+a.width/2))+'px');
      h1.style.setProperty('--dy',(b.top-(a.top+a.height*0.55))+'px');
      h1.classList.add('fly'); setTimeout(()=>h1.classList.add('landed'),2650); }, 1150);
  })();
  const sf = document.getElementById('signup');
  if (sf) sf.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = sf.querySelector('button'), msg = document.getElementById('joinmsg');
    btn.disabled = true; btn.textContent = 'Sending…';
    try {
      const r = await fetch('https://formsubmit.co/ajax/products000001@gmail.com', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(Object.fromEntries(new FormData(sf))) });
      if (!r.ok) throw 0;
      msg.textContent = 'You’re on the list. Thank you!'; sf.reset(); btn.textContent = 'Done ✓';
    } catch (err) { sf.submit(); }
  });
