# Arbeitsauftrag: tarifwerk.eu auf 10/10 bringen

**Für:** den Claude-Chat mit Zugriff auf den Code von www.tarifwerk.eu (Next.js, Firebase App Hosting)
**Von:** Prüfung der Live-Seite am 02.11.2026 (alle 33 Seiten aus der Sitemap, Desktop und Handy)
**Umfang:** nur die Punkte, die wirklich zählen, nach Wichtigkeit sortiert

---

## Regeln für die Umsetzung

1. **Das Logo-Design wird nicht verändert.** Keine neue Form, keine neuen Farben, kein Neuzeichnen, kein Entfernen des Chrom-Looks. Erlaubt ist nur, was die Erkennbarkeit verbessert: Größe, Zuschnitt, Hintergrund beim Favicon, Bildqualität (siehe Punkt 1).
2. **Keine Inhalte erfinden.** Berater-Texte, Fotos, Telefonnummern, Registernummern und Rechtstexte kommen von Marvin. Fehlt etwas, nachfragen statt Platzhalter live zu stellen.
3. Auf einem eigenen Branch arbeiten. Marvin das Ergebnis zeigen, bevor es live geht.
4. Nach jedem Punkt: Build und Lint laufen lassen, die betroffenen Seiten auf Desktop (1440 px) und Handy (390 px) im Browser prüfen.

---

## 1. Logo gut erkennbar machen (Design bleibt gleich)

### Problem
- Im Header wird `tarifwerk-logo.png` (Schriftzug + orange Linie + „Beratung auf Augenhöhe“) auf **148 × 44 px** (Desktop) bzw. **94 × 28 px** (Handy) verkleinert. Die Unterzeile ist dadurch nur noch **3–5 px hoch** und nicht lesbar. Auch der Schriftzug selbst wird dadurch kleiner, als er sein müsste.
- Das Favicon (`/favicon.svg`, `/icon-48.png`) hat einen **transparenten Hintergrund**. Der silberne Teil des Zeichens verschwindet in einer hellen Browser-Tab-Leiste.
- `/favicon.ico` fehlt (404). Browser fragen diese Datei automatisch ab.
- Der Logo-Link hat als zugänglichen Namen nur **„, zur Startseite“** (Bild `alt=""`, Screenreader-Text beginnt mit Komma). „TarifWerk“ fehlt.

### Lösung
Fertige Dateien aus dem unveränderten Original liegen im Repo `pyn7r68zsg-lgtm/TarifWerk`, Branch `claude/tarifwerk-website-review-4mk5bw`, Ordner `logo-lesbar/` (Marvin kann sie auch direkt im Chat hochladen):

| Datei | Was ist anders als vorher | Ziel im Projekt |
| --- | --- | --- |
| `tarifwerk-schriftzug.png` | Originaler Schriftzug, nur **zugeschnitten** (ohne Linie und Unterzeile), 959 × 169 px | `public/assets/brand/tarifwerk-schriftzug.png` (neu, das alte Logo bleibt für den Footer) |
| `favicon.ico` | Originalzeichen auf dem dunklen Grund des App-Icons (#060b16), 16/32/48 px, leicht nachgeschärft | `public/favicon.ico` bzw. `app/favicon.ico` |
| `icon-48.png` | wie oben, 48 px | ersetzt `public/icon-48.png` |
| `icon-192.png` | wie oben, 192 px | neu, für das Manifest |
| `apple-icon.png` | Zeichen etwas größer im Quadrat (vorher sehr kleiner Rand) | ersetzt `apple-icon.png` |

**Header (alle Seiten):**
- Statt `tarifwerk-logo.png` den neuen `tarifwerk-schriftzug.png` verwenden. Das Zeichen (`tarifwerk-zeichen.png`) bleibt, ebenso die Hover-Animation.
- Größen:
  - Desktop: Zeichen **40 px** hoch, Schriftzug **26 px** hoch
  - Handy: Zeichen **32 px** hoch, Schriftzug **20 px** hoch
  - Header-Höhe nicht vergrößern, es passt in die bestehende Zeile.
- `width`/`height` passend zum echten Seitenverhältnis setzen (Schriftzug 959 : 169). Sonst lädt `next/image` falsche Größen.
- Barrierefreiheit: Am Link `aria-label="TarifWerk – zur Startseite"` setzen, die Bilder darin `alt=""`. Das sr-only „, zur Startseite“ entfernen.

```tsx
<Link href="/" aria-label="TarifWerk – zur Startseite" className="group inline-flex min-h-11 items-center gap-2 sm:gap-3">
  <Image src="/assets/brand/tarifwerk-zeichen.png" alt="" width={240} height={183}
         className="h-8 w-auto sm:h-10 transition-transform ..." priority />
  <Image src="/assets/brand/tarifwerk-schriftzug.png" alt="" width={959} height={169}
         className="h-5 w-auto sm:h-[26px]" priority />
</Link>
```

**Footer:** Das vollständige Logo **mit** Unterzeile bleibt dort, aber mindestens **320 px breit** darstellen. Darunter ist die Unterzeile nicht lesbar. Wenn der Platz fehlt, auch dort Zeichen + Schriftzug verwenden.

**Favicon im `<head>`:**

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/icon-48.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="/apple-icon.png" sizes="180x180">
```

Bei App-Router-Konventionen (`app/icon.png`, `app/apple-icon.png`, `app/favicon.ico`) dort ersetzen. Die alte `public/favicon.svg` (enthält nur ein eingebettetes PNG mit transparentem Hintergrund) löschen oder nicht mehr verlinken. Im Manifest `icon-192.png` ergänzen.

**Prüfen:**
- Header-Screenshot Desktop und Handy: Schriftzug klar lesbar, keine Unterzeile im Header.
- `curl -I https://www.tarifwerk.eu/favicon.ico` liefert 200.
- Favicon in hellem und dunklem Browser-Tab erkennbar.

Vorher/nachher-Bilder: `logo-lesbar/vorschau/`.

---

## 2. Anfrageformular: Upload und weniger Pflichtfelder

### Problem
- Die ganze Seite verspricht „Vertrag schicken – Foto, PDF oder Screenshot genügt“, aber `/anfrage` (und das gleiche Formular auf den Berater-Seiten) hat **kein Upload-Feld**.
- **Name, E-Mail und Telefon sind alle Pflicht**, auch wenn jemand „E-Mail“ als Kontaktweg wählt. Das kostet Anfragen.

### Lösung
**a) Upload in Schritt 2** („Dein Kontakt“), über dem Textfeld „Was sollten wir vorab … wissen?“:
- `<input type="file" accept="image/jpeg,image/png,image/webp,image/heic,application/pdf" multiple>` mit sichtbarem Label „Vertrag oder Angebot (optional)“ und Hinweis „Foto, PDF oder Screenshot · max. 10 MB pro Datei · höchstens 5 Dateien“.
- Ausgewählte Dateien als Liste mit Namen, Größe und Entfernen-Knopf anzeigen.
- **Serverseitig:** MIME-Typ anhand der Datei-Signatur prüfen (nicht nur der Endung), 10 MB pro Datei und 5 Dateien als Grenze.
- **Speicherung:** in einem **privaten** Speicher (z. B. Firebase Storage mit Regeln, die nur dem Server Zugriff geben), nie unter einer öffentlichen URL. In der Anfrage-Benachrichtigung an den Berater nur einen zeitlich begrenzten Link (Signed URL) mitschicken.
- **Löschen:** automatisch nach 90 Tagen (oder wenn die Anfrage abgeschlossen ist).
- **Datenschutzerklärung:** einen Abschnitt zum Datei-Upload ergänzen (Zweck, Speicherort, Speicherdauer). **Den Text vor dem Live-Gang von Marvin freigeben lassen.**

**b) Pflichtfelder abhängig vom Kontaktweg** („Wie möchtest du sprechen?“: WhatsApp, Telefon, E-Mail, Video-Call, Vor Ort):
- Pflicht immer: **Name** und Einwilligung.
- **Telefon** Pflicht bei WhatsApp, Telefon, Video-Call, Vor Ort.
- **E-Mail** Pflicht nur bei E-Mail, sonst optional.
- Labels anpassen („E-Mail (optional)“). Die gleiche Logik serverseitig prüfen.

**c) Layout:** Unten in Schritt 1 stoßen der Hinweis „So verdienen wir…“ und der Button „Weiter zum Kontakt“ fast aneinander. Den Hinweis über den Button setzen oder Abstand (`gap-4`) einbauen.

**Prüfen:** Testanfrage mit PDF und Foto auf dem Handy. Die Datei kommt beim Berater an und ist ohne Link nicht öffentlich abrufbar. Eine Anfrage nur mit Name + E-Mail (Kontaktweg E-Mail) geht durch.

---

## 3. Berater-Profile korrigieren

### Fehler, die sofort behoben werden müssen

| Wo | Aktuell | Richtig |
| --- | --- | --- |
| `/berater/ian`: Title, H1, Karten auf `/berater` und `/ueber-uns`, „Ein Gespräch mit ian“, „ian bestätigt …“ | **ian** Daniel Daake | **Ian** Daniel Daake |
| `/berater/ian`, Zitat | „immer Weiter machen, Niemals Aufgeben.“ | „Immer weitermachen, niemals aufgeben.“ |
| `/berater/ian`, Telefon-Anzeige | 015252033327 | 0152 52033327 |
| alle Berater-Karten, `tel:`-Links | `tel:015252033327` usw. | `tel:+4915252033327` (internationales Format) |
| `/berater/kubilay` | TarifWerk-Logo als Profilbild | echtes Foto (**von Marvin anfordern**) |
| `/berater/anna` | kein Anruf-Button | Nummer **von Marvin anfordern** |

Am besten an der Quelle korrigieren (Datenbank/Datei der Berater). Zusätzlich eine Formatierungsfunktion für Telefonnummern bauen (Anzeige mit Leerzeichen, Link immer `+49…`).

### Bio-Texte
Jeder Text beginnt heute mit dem Alter („ist 22/23/25/29 Jahre alt“). Bei Themen wie Versicherungen, Immobilien und Gold wirkt das unerfahren. **Nur den Alterssatz umformulieren bzw. entfernen**, den Rest nicht umschreiben. Neue Texte liefert Marvin.

### Profilbilder zu groß
Alle Beraterfotos kommen über `/api/advisors/{id}/image` als **1200 × 1200 px WebP (~77 KB)**. Angezeigt werden sie als 56–64-px-Kreis. Auf `/berater` sind das sechs Bilder, rund 450 KB unnötig.
- In der Route einen Breiten-Parameter einbauen und mit `sharp` skalieren:

```ts
const w = Math.min(Math.max(Number(searchParams.get("w")) || 256, 32), 1200);
const out = await sharp(original).resize(w, w, { fit: "cover" }).webp({ quality: 80 }).toBuffer();
```

- Für Avatare `?w=128` (2× für Retina) anfragen, auf der Profilseite `?w=320`.
- Die bestehende `Cache-Control: immutable`-Logik mit `?v=` beibehalten.

---

## 4. Server-Antwortzeit (wichtig für Google und Gefühl beim Öffnen)

### Problem
Jede HTML-Seite antwortet nach **0,55–1,15 s** und kommt mit `cache-control: private, no-store`. Das CDN von Firebase kann also nichts zwischenspeichern.

### Ursache (sehr wahrscheinlich)
Die CSP verwendet einen **Nonce pro Anfrage** (`script-src 'self' 'nonce-…' 'strict-dynamic'`, gesetzt in Middleware/Proxy). Damit zwingt Next.js **jede Seite in dynamisches Rendering**.

### Lösung (in dieser Reihenfolge prüfen)
1. **Option A, bevorzugt:** Für die öffentlichen Marketing-Seiten auf eine **hash-basierte CSP** umstellen (`experimental.sri` in `next.config`, falls mit der verwendeten Next-Version und dem Bundler kompatibel). Den Nonce nur noch für `/portal` und `/api` setzen. In der Middleware/Proxy den `matcher` entsprechend einschränken.
2. **Option B:** Wenn A nicht geht: CSP für öffentliche Seiten statisch mit `script-src 'self' 'unsafe-inline'` – **nur mit Marvins Zustimmung**, weil es die Sicherheit senkt.
3. Danach öffentliche Seiten statisch bzw. mit `export const revalidate = 3600` ausliefern.

**Prüfen:** `curl -sI https://www.tarifwerk.eu/` zeigt keinen `no-store` mehr, beim zweiten Aufruf `cdn-cache-status: hit`, TTFB unter 200 ms. Die CSP-Sicherheit (keine Inline-Skripte ohne Hash/Nonce) darf nicht schlechter werden.

---

## 5. Startseite kürzen

### Problem
Mobil ist die Startseite ca. **13.700 px** lang (rund 16 Bildschirme). Der 3-Schritte-Ablauf steht zweimal darauf: in der Hero-Karte „In drei Schritten zu Klarheit“ und bei „Vertrag schicken / Wir prüfen / Du gibst frei“. Mehrere Bereiche wiederholen Inhalte anderer Seiten.

### Lösung: neue Reihenfolge
1. Hero (Claim, CTA, Google-Bewertung). Die Schritte-Karte im Hero ersetzen durch die Karte mit Gründerfoto und dem Satz „Marvin liest deine Anfrage persönlich – täglich 8 bis 22 Uhr erreichbar“.
2. „Schon ein Vertrag oder Angebot vor dir?“ + Kostenrechner (bleibt, mit den drei Schritten)
3. „Dort anfangen, wo der nächste Schritt zählt“ (drei Hauptthemen, bleibt)
4. „Vertrauen entsteht auch durch das, was man bewusst nicht macht“ + „So verdienen wir Geld“ (bleibt)
5. Google-Bewertungen (bleibt)
6. FAQ (bleibt)
7. Abschluss „Schick uns deinen Vertrag“ + Footer

**Von der Startseite entfernen** (Inhalte gibt es schon auf eigenen Seiten):
- „Ein Haus. Acht Themen. Ein Ansprechpartner.“ (Haus-Grafik) → auf `/leistungen` verschieben, falls dort nicht vorhanden
- 6er-Raster „Was TarifWerk anders macht“ → auf die 3 stärksten Punkte kürzen oder nach `/ueber-uns`
- „Zufrieden? Gib es weiter.“ (Freunde werben) → nur im Footer verlinken
- „Wir automatisieren Ihr Unternehmen mit KI“ → nur im Business-Modus zeigen
- „Worum geht es bei dir?“ (Themen-Auswahl) → doppelt mit `/anfrage`

**Prüfen:** Mobile Seitenlänge mindestens 30 % kürzer. Alle entfernten Inhalte sind über Menü oder Footer erreichbar, kein Link läuft ins Leere.

---

## 6. Navigation und Telefon im Header

- **Hauptmenü heute:** Leistungen · Kostenrechner · Ablauf · Berater · Berater werden
- **Neu:** Leistungen · Kostenrechner · Berater · Ratgeber · Über uns
- „Berater werden“ nur noch im Footer (Bereich „Partner & Team“, steht dort schon).
- **Telefonnummer** `0157 82301076` als `tel:+4915782301076`-Link in den Desktop-Header (ab `lg`, links vom CTA). „Täglich 8–22 Uhr erreichbar“ ist ein Vorteil und muss sichtbar sein.
- Das Handy-Menü und die untere Leiste (WhatsApp / Vertrag prüfen / Anrufen) bleiben.

---

## 7. 404-Seite

### Problem
Die 404-Seite hat kein Menü und keinen Footer. Ihr `<title>` ist identisch mit der Startseite. Sie siezt („starten Sie“), der Rest der Privatseite duzt.

### Lösung
- `app/not-found.tsx` innerhalb des Layouts mit Header/Footer rendern.
- `metadata.title = "Seite nicht gefunden | TarifWerk"`
- Text: „Kein Drama. Starte auf der Startseite oder schau direkt hier:“
- Darunter Links zu: Vertrag prüfen lassen, Leistungen, Kostenrechner, Kontakt.
- Statuscode bleibt 404.

---

## 8. Weiterleitung auf www

Heute: `http://tarifwerk.eu` → 301 → `https://tarifwerk.eu` → **302** → `https://www.tarifwerk.eu`. Google wertet eine 302 als vorübergehend.

**Ziel:** von jeder Variante **ein** 301/308 direkt auf `https://www.tarifwerk.eu/…`
- Zuerst in der Firebase Console unter **App Hosting → Domains** prüfen, wie `tarifwerk.eu` eingerichtet ist (die 302 kommt von dort).
- Wenn die Plattform keine dauerhafte Weiterleitung anbietet: `tarifwerk.eu` als normale Domain verbinden und in `next.config` umleiten:

```js
async redirects() {
  return [{
    source: "/:path*",
    has: [{ type: "host", value: "tarifwerk.eu" }],
    destination: "https://www.tarifwerk.eu/:path*",
    permanent: true,
  }];
}
```

---

## 9. Erstinformation (erst umsetzen, wenn Marvin die Daten liefert)

`/erstinformation` nennt heute keinen einzigen Vermittler. Wenn Marvin die Angaben der Fachpartner liefert, pro Fachpartner einen Block anlegen:
- Name/Firma
- Anschrift
- Status nach GewO (§ 34d, § 34c bzw. § 34i)
- Registernummer mit Link auf www.vermittlerregister.info
- Zuständige IHK
- Schlichtungsstellen

**Keine Platzhalter live stellen.** Der fertige Text muss vorher von einem Anwalt geprüft sein (das klärt Marvin).

---

## Abschlussprüfung

- [ ] Build und Lint ohne Fehler
- [ ] Alle Seiten aus `sitemap.xml` liefern 200, `/favicon.ico` liefert 200, eine unbekannte URL liefert 404 mit eigenem Titel
- [ ] Header-Logo auf Desktop und Handy klar lesbar, Logo-Design unverändert
- [ ] Testanfrage mit Upload auf dem Handy erfolgreich
- [ ] Keine Konsolenfehler, WCAG-Test (axe) ohne Fehler wie bisher
- [ ] HTML-Antwortzeit unter 200 ms, kein `no-store` auf öffentlichen Seiten
- [ ] Marvin hat Screenshots von Startseite, Header und Formular gesehen und freigegeben
