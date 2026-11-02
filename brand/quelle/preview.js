// Aufruf aus dem Ordner brand/:  node quelle/preview.js "$PWD/svg" vorschau/uebersicht.png
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
const [,,OUT,PNG]=process.argv;
const f=n=>'file://'+path.join(OUT,n);
const html=`<html><body style="margin:0;font-family:sans-serif">
<div style="background:#060b16;padding:30px;display:flex;flex-wrap:wrap;gap:40px;align-items:center">
 <img src="${f('tarifwerk-zeichen-dark.svg')}" height="120">
 <img src="${f('tarifwerk-logo-horizontal-dark.svg')}" height="60">
 <img src="${f('tarifwerk-logo-dark.svg')}" height="80">
 <img src="${f('tarifwerk-logo-gestapelt-dark.svg')}" height="220">
</div>
<div style="background:#f4f6fa;padding:30px;display:flex;flex-wrap:wrap;gap:40px;align-items:center">
 <img src="${f('tarifwerk-zeichen-light.svg')}" height="120">
 <img src="${f('tarifwerk-logo-horizontal-light.svg')}" height="60">
 <img src="${f('tarifwerk-logo-light.svg')}" height="80">
 <img src="${f('tarifwerk-logo-gestapelt-light.svg')}" height="220">
</div>
<div style="background:#060b16;padding:14px 120px;display:flex;align-items:center;gap:40px;color:#cbd5e1;font-size:15px">
 <img src="${f('tarifwerk-logo-horizontal-dark.svg')}" height="34"><span>Leistungen</span><span>Kostenrechner</span><span>Ablauf</span><span>Berater</span>
</div>
<div style="background:#fff;padding:20px;display:flex;gap:20px;align-items:end">
 <img src="${f('favicon.svg')}" width="16"><img src="${f('favicon.svg')}" width="32"><img src="${f('favicon.svg')}" width="48"><img src="${f('tarifwerk-icon.svg')}" width="120"><img src="${f('tarifwerk-icon.svg')}" width="180">
</div></body></html>`;
fs.writeFileSync(path.join(OUT,'..','preview.html'),html);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1500,height:800}});
await p.goto('file://'+path.join(OUT,'..','preview.html'));await p.waitForTimeout(300);await p.screenshot({path:PNG,fullPage:true});await b.close();})();
