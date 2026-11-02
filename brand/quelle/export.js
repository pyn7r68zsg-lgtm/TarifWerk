// Aufruf aus dem Ordner brand/:  node quelle/export.js .
// Erzeugt brand/png/* (Dateinamen wie auf der Live-Seite) und das OG-Bild.
const { chromium } = require('playwright'); const path=require('path'); const fs=require('fs');
const [,,BASE]=process.argv; const OUT=path.join(BASE,'svg'); const PNG=path.join(BASE,'png'); fs.mkdirSync(PNG,{recursive:true});
const jobs=[
 // [svg, ausgabe, breite, hoehe(optional)]
 ['tarifwerk-zeichen-dark.svg','tarifwerk-zeichen.png',480],
 ['tarifwerk-zeichen-light.svg','tarifwerk-zeichen-hell.png',480],
 ['tarifwerk-wortmarke-dark.svg','tarifwerk-logo.png',960],
 ['tarifwerk-logo-horizontal-dark.svg','tarifwerk-logo-horizontal.png',960],
 ['tarifwerk-logo-horizontal-light.svg','tarifwerk-logo-horizontal-hell.png',960],
 ['tarifwerk-logo-gestapelt-dark.svg','tarifwerk-logo-gestapelt.png',1200],
 ['tarifwerk-logo-gestapelt-light.svg','tarifwerk-logo-gestapelt-hell.png',1200],
 ['tarifwerk-icon.svg','tarifwerk-icon-512.png',512,512],
 ['tarifwerk-icon-quadrat.svg','apple-icon.png',180,180],
 ['tarifwerk-icon-quadrat.svg','icon-maskable-512.png',512,512],
 ['favicon.svg','icon-48.png',48,48],
 ['favicon.svg','icon-32.png',32,32],
 ['favicon.svg','icon-16.png',16,16],
 ['tarifwerk-icon.svg','icon-192.png',192,192],
];
(async()=>{const b=await chromium.launch();
for(const [src,dst,w,h0] of jobs){
  const svg=fs.readFileSync(path.join(OUT,src),'utf8'); const vb=svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const h=h0||Math.round(w*(+vb[2])/(+vb[1]));
  const p=await b.newPage({viewport:{width:w,height:h}});
  await p.setContent(`<style>html,body{margin:0;background:transparent}img{display:block;width:${w}px;height:${h}px}</style><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}">`);
  await p.waitForTimeout(150);
  await p.screenshot({path:path.join(PNG,dst),omitBackground:true}); await p.close(); console.log(dst,w,h);
}
const p=await b.newPage({viewport:{width:1200,height:630}});
await p.goto('file://'+path.join(BASE,'quelle','og.html')); await p.waitForTimeout(500);
await p.screenshot({path:path.join(PNG,'og-tarifwerk-logo.jpg'),type:'jpeg',quality:90}); console.log('og-tarifwerk-logo.jpg');
await b.close();})();
