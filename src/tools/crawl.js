const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const base='http://localhost:4175';
  const pages=['/','/retired-husband-syndrome','/privacy','/terms','/refund','/contact'];
  const issues=[]; const links=new Set();
  for (const w of [320,375,768,1024,1440]) for (const u of pages) {
    const p = await b.newPage({ viewport:{width:w,height:900} });
    p.on('console', m=>{ if(m.type()==='error') issues.push(`console ${u}@${w}: ${m.text()}`); });
    p.on('pageerror', e=>issues.push(`jserr ${u}@${w}: ${e.message}`));
    p.on('response', r=>{ if(r.status()>=400) issues.push(`${r.status()} ${r.url()} on ${u}`); });
    await p.goto(base+u,{waitUntil:'networkidle'}); await p.waitForTimeout(300);
    const r = await p.evaluate(()=>{
      const o={overflow:document.documentElement.scrollWidth-innerWidth, links:[], badAnchors:[], noAlt:[], brokenImg:[], wide:[]};
      document.querySelectorAll('a[href]').forEach(a=>o.links.push(a.getAttribute('href')));
      document.querySelectorAll('a[href^="#"]').forEach(a=>{const id=a.getAttribute('href').slice(1); if(id && !document.getElementById(id)) o.badAnchors.push(id);});
      document.querySelectorAll('img').forEach(i=>{ if(!i.hasAttribute('alt')) o.noAlt.push(i.src.slice(0,60)); if(i.complete && i.naturalWidth===0) o.brokenImg.push(i.src.slice(0,60)); });
      if (document.documentElement.scrollWidth>innerWidth) document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect(); if(r.right>innerWidth+1) o.wide.push(e.tagName+'.'+e.className);});
      o.title=document.title; o.h1=document.querySelectorAll('h1').length; o.lang=document.documentElement.lang; o.desc=!!document.querySelector('meta[name=description]');
      return o; });
    if (r.overflow>0) issues.push(`overflow ${r.overflow}px ${u}@${w}: ${r.wide.slice(0,4)}`);
    if (r.badAnchors.length) issues.push(`bad anchors ${u}: ${r.badAnchors}`);
    if (r.noAlt.length) issues.push(`no alt ${u}: ${r.noAlt}`);
    if (r.brokenImg.length) issues.push(`broken img ${u}: ${r.brokenImg}`);
    if (w===1440) { console.log(u, '|', r.title, '| h1:', r.h1, '| lang:', r.lang, '| desc:', r.desc); r.links.forEach(l=>links.add(l)); }
    await p.close();
  }
  for (const l of links) { if (l.startsWith('/') ) { const path=l.split('#')[0]||'/'; const res=await (await b.newPage()).request.get(base+path); if(res.status()>=400) issues.push(`link ${l} -> ${res.status()}`);} }
  console.log('external/other links:', [...links].filter(l=>!l.startsWith('/')&&!l.startsWith('#')));
  // interactive
  const p = await b.newPage({ viewport:{width:1280,height:900} }); await p.goto(base+'/');
  await p.click('.chip[data-f="family"]'); const vis=await p.$$eval('#books .bk', e=>e.filter(x=>x.style.display!=='none').length); console.log('family filter shows', vis);
  await p.click('.chip[data-f="life"]'); console.log('self-help shows', await p.$$eval('#books .bk', e=>e.filter(x=>x.style.display!=='none').length));
  const q = await b.newPage({ viewport:{width:1280,height:900} }); await q.goto(base+'/retired-husband-syndrome');
  await q.click('.buyrow .buy'); console.log('dialog open:', await q.$eval('#checkout', d=>d.open)); await q.click('#close-checkout'); console.log('dialog closed:', !(await q.$eval('#checkout', d=>d.open)));
  console.log('ISSUES', issues.length); [...new Set(issues)].forEach(i=>console.log(' -', i));
  await b.close(); })();
