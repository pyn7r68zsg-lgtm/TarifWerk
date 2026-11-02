# TarifWerk – Umsetzungsplan zur 10/10-Webseite

Grundlage: Prüfung der Live-Seite www.tarifwerk.eu am 02.11.2026 (alle 33 Seiten der Sitemap, Desktop und Handy, Ladezeit, WCAG-Test, SEO, Header, Formular, Rechtstexte).

**Wichtig:** Der Quellcode der Webseite liegt in keinem der GitHub-Repos, auf die Claude Zugriff hat (`TarifWerk` und `Tarifwerk.` sind leer, `tarif` enthält nur Notizen). Die Seite läuft laut Server-Headern auf **Firebase App Hosting**, und das baut normalerweise aus einem GitHub-Repo. Damit alle Punkte unten direkt im Code umgesetzt werden können, siehe [„Code freigeben“](#code-freigeben) ganz unten.

Legende: ✅ erledigt (in diesem Repo) · 💻 braucht den Webseiten-Code · 👤 braucht dich (Inhalte, Fotos, Entscheidungen, Anwalt)

## Übersicht

| # | Punkt | Status |
| --- | --- | --- |
| 1 | Upload (Foto/PDF) im Anfrageformular | 💻 |
| 2 | Weniger Pflichtfelder im Formular | 💻 |
| 3 | Angebot schärfen (drei Kernthemen vorne, KI/Business trennen) | 👤 + 💻 |
| 4 | Berater-Profile korrigieren und professioneller machen | 👤 + 💻 |
| 5 | Erstinformation vollständig machen | 👤 (Anwalt) + 💻 |
| 6 | Neues Logo, Favicon, App-Icons, OG-Bild | ✅ (Einbau 💻) |
| 7 | Startseite kürzen, doppelte Abläufe entfernen | 💻 |
| 8 | Navigation und Telefonnummer im Header | 💻 |
| 9 | Du/Sie vereinheitlichen | 💻 |
| 10 | 404-Seite mit Menü, eigenem Titel, Du-Form | 💻 |
| 11 | Server-Antwortzeit (Caching) | 💻 |
| 12 | Gründerfoto 1200 × 1200 px für 56-px-Kreis | 💻 |
| 13 | Weiterleitung `tarifwerk.eu` → `www` als ein 301 | 💻 / Firebase |
| 14 | Mehr Ratgeber- und Städteseiten | 👤 + 💻 |
| 15 | Sitemap mit echten Änderungsdaten | 💻 |
| 16 | `bluetooth` aus Permissions-Policy entfernen | 💻 |
| 17 | Mehr Google-Bewertungen sammeln | 👤 |
| 18 | Abstand unten im Formular | 💻 |
| 19 | `/favicon.ico` fehlt (404) | ✅ (Datei liegt bereit) |

## ✅ Bereits erledigt (in diesem Repo)

- **Logo-System** in [`brand/`](brand/README.md): Zeichen, Header-Logo, Logo mit Unterzeile, gestapelte Version, jeweils für dunklen und hellen Hintergrund, als SVG und PNG.
- **Austauschdateien** in [`public/`](public) mit denselben Pfaden wie live:
  - `public/favicon.ico` (neu, live fehlt die Datei → 404), `favicon.svg` (echter Vektor statt eingebettetem PNG)
  - `public/icon-48.png`, `icon-192.png`, `apple-icon.png`, `icon-maskable-512.png`
  - `public/og-tarifwerk-logo.jpg` (1200 × 630, Vorschaubild für WhatsApp, LinkedIn usw.)
  - `public/assets/brand/tarifwerk-logo.png`, `tarifwerk-zeichen.png`, `tarifwerk-icon-512.png` + SVG-Versionen
  - `public/manifest.webmanifest` mit 192er-, 512er- und maskable-Icon

**Einbau:** Dateien aus `public/` in den `public/`-Ordner des Webseiten-Projekts kopieren. Falls es im Projekt `app/icon.png`, `app/apple-icon.png`, `app/favicon.ico` oder `app/manifest.ts` gibt, haben diese Vorrang und müssen dort ersetzt werden. Den Header auf **ein** SVG-Logo umstellen (Code in [`brand/README.md`](brand/README.md#einbau-in-die-webseite-nextjs)).

---

## 🔴 Kritisch

### 1. Upload im Anfrageformular 💻

**Problem:** Überall steht „Vertrag schicken – Foto, PDF oder Screenshot genügt“, aber `/anfrage` hat kein Upload-Feld.

**Lösung:** In Schritt 2 des Formulars ein optionales Upload-Feld:

```tsx
<label className="block text-sm font-medium" htmlFor="vertrag">
  Vertrag oder Angebot (optional)
</label>
<input
  id="vertrag"
  name="vertrag"
  type="file"
  accept="image/*,application/pdf"
  multiple
  className="..."
/>
<p className="text-xs text-steel">Foto, PDF oder Screenshot · max. 10 MB pro Datei · höchstens 5 Dateien</p>
```

Auf dem Server: Dateityp und Größe prüfen (nur `image/jpeg|png|webp|heic`, `application/pdf`, max. 10 MB), in einem **nicht öffentlichen** Speicher ablegen (z. B. Firebase Storage mit Regeln „nur Server“) und nach Abschluss der Anfrage oder spätestens nach 90 Tagen löschen. In der Datenschutzerklärung ergänzen: Zweck, Speicherdauer, Speicherort. Falls der Upload nicht sofort machbar ist, als Übergang direkt im Formular einen Knopf „Vertrag per WhatsApp schicken“ mit `https://wa.me/4915782301076?text=...` anbieten.

### 2. Weniger Pflichtfelder 💻

**Problem:** Name, E-Mail **und** Telefon sind alle Pflicht.

**Lösung:** Pflicht sind nur Name + **ein** Kontaktweg, abhängig von „Wie möchtest du sprechen?“:

```ts
const telefonPflicht = ["whatsapp", "telefon", "video"].includes(kontaktweg);
const emailPflicht = kontaktweg === "email";
// <input name="phone" required={telefonPflicht} />
// <input name="email" required={emailPflicht} />
```

Die Validierung muss serverseitig genauso laufen.

### 3. Angebot schärfen 👤 + 💻

**Problem:** Handyvertrag, Gold, Alarmanlage, Klimaanlage, Immobilien und eine KI-Agentur für Firmen auf einer Seite wirken wie ein Gemischtwarenladen. Das kostet Vertrauen.

**Vorschlag:**
- Startseite: nur **Strom & Gas, Internet & Mobilfunk, Solar/PV & Wärmepumpe** als Hauptthemen. Die übrigen Bereiche als kleine Liste „Außerdem helfen wir bei …“ unter `/leistungen`.
- Versicherungen und Immobilien klar als „über zugelassene Fachpartner“ kennzeichnen (machst du schon, gut).
- **KI & Digitalisierung** auf eine eigene Domain oder Unterdomain (z. B. `ki.tarifwerk.eu` oder eigene Marke). Mindestens: aus Hauptmenü und Startseite der Privatkunden entfernen und nur im „Business“-Modus zeigen.
- **Edelmetalle** auf der Startseite weglassen. Bei Geldanlage wirkt ein Tarifberater schnell unseriös.

👤 Diese Entscheidung musst du treffen. Danach kann der Code angepasst werden.

### 4. Berater-Profile 👤 + 💻

Sofort zu korrigieren (Datenfehler):

| Seite | Aktuell | Richtig |
| --- | --- | --- |
| `/berater/ian` | „ian Daniel Daake“ (Titel, H1, „Ein Gespräch mit ian“, „ian bestätigt…“) | „Ian Daniel Daake“, „Ein Gespräch mit Ian“ |
| `/berater/ian` | „immer Weiter machen, Niemals Aufgeben.“ | „Immer weitermachen, niemals aufgeben.“ |
| `/berater/ian` | Telefon „015252033327“ | „0152 52033327“ (Link `tel:+4915252033327`) |
| `/berater/kubilay` | TarifWerk-Logo als Profilbild | echtes Foto 👤 |
| `/berater/anna` | kein Anruf-Button | Telefonnummer ergänzen 👤 |

Am besten in den Daten (Datenbank/JSON) korrigieren und zusätzlich im Code den Anzeigenamen absichern:

```ts
const anzeigename = (s: string) => s.replace(/(^|\s)\p{Ll}/gu, (m) => m.toUpperCase());
```

**Bio-Texte neu schreiben** 👤 – ohne Alter am Anfang, dafür mit dem, was Kunden Sicherheit gibt. Vorlage:

> **[Vorname] berät seit [Jahr] zu [Schwerpunkt 1] und [Schwerpunkt 2].** Bisher begleitet: [Zahl] Haushalte in [Region]. Vorher [Beruf/Erfahrung, die zur Beratung passt, z. B. Kundenkontakt, Verantwortung, Technik]. Schulungen: [z. B. Energiemarkt, Glasfaser, PV-Grundlagen]. Was Kunden an [Vorname] schätzen: „[kurzes echtes Zitat aus einer Google-Bewertung]“.

Pro Berater außerdem: eigene Bewertungen (wenn vorhanden), Sprachen und echte Verfügbarkeit.

### 5. Erstinformation vollständig machen 👤 (Anwalt) + 💻

**Problem:** `/erstinformation` nennt keinen einzigen Vermittler, sondern nur, dass man die Angaben später bekommt. Für eine Seite, die Versicherungen, Immobilien und Finanzierungen anbietet, reicht das für Vertrauen und Google nicht.

**Vorschlag:** Pro Fachpartner ein Block (Angaben vom Fachpartner einholen):

```
Fachpartner für Versicherungen
[Name, Firma]
[Anschrift]
Status: [z. B. Versicherungsmakler mit Erlaubnis nach § 34d Abs. 1 GewO]
Vermittlerregister-Nr.: [D-XXXX-XXXXX-XX] · www.vermittlerregister.info
Zuständige Stelle: [IHK …]
Schlichtungsstellen: Versicherungsombudsmann e. V., Ombudsmann Private Kranken- und Pflegeversicherung
```

Entsprechend für Immobilien/Finanzierungen (§ 34c bzw. § 34i GewO). Zusätzlich klar beschreiben, was TarifWerk selbst tut („Wir stellen nur den Kontakt her und beraten nicht zu Versicherungen“).

👤 **Das ist keine Rechtsberatung.** Lass Erstinformation, Impressum, AGB (vor allem das Empfehlungsprogramm „bis zu 1.000 €“) und Datenschutz (inkl. KI-Chat und Datei-Upload) von einem Anwalt für Vermittlerrecht prüfen.

---

## 🟠 Wichtig

### 7. Startseite kürzen 💻

Mobil ist die Startseite etwa 13.700 px lang (rund 16 Bildschirme). Der 3-Schritte-Ablauf kommt doppelt vor (Hero-Karte „In drei Schritten zu Klarheit“ und „Vertrag schicken / Wir prüfen / Du gibst frei“) und auf „Über uns“ ein drittes Mal.

**Neue Reihenfolge (Vorschlag):**
1. Hero (Claim + CTA + Google-Bewertung + Gründerfoto). Die Schritte-Karte im Hero ersetzen durch das Gründerfoto mit einem Satz.
2. „Schon ein Vertrag vor dir?“ + Kostenrechner (behalten, das ist stark)
3. Drei Kernthemen
4. „So verdienen wir Geld“ (behalten, das schafft Vertrauen)
5. Google-Bewertungen
6. FAQ (5 Fragen)
7. Abschluss-CTA + Footer

**Raus von der Startseite:** „Ein Haus. Acht Themen.“ (Haus-Grafik → nach `/leistungen`), 6er-Grid „Was TarifWerk anders macht“ (auf 3 Punkte kürzen), „Freunde werben“ und „KI für Unternehmen“ (eigene Seiten, im Footer verlinkt), „Worum geht es bei dir?“ (doppelt mit `/anfrage`). Ziel: etwa 30 % kürzer.

### 8. Navigation und Telefon im Header 💻

Aktuell: `Leistungen · Kostenrechner · Ablauf · Berater · Berater werden`

Neu: `Leistungen · Kostenrechner · Berater · Ratgeber · Über uns` und rechts **`0157 82301076`** (als `tel:`-Link, ab `lg` sichtbar) plus CTA „Vertrag prüfen lassen“. „Berater werden“ in den Footer unter „Partner & Team“ (dort steht es schon).

### 9. Du/Sie vereinheitlichen 💻

- Privatbereich: überall **du**. Abweichung gefunden auf der **404-Seite** („starten Sie“).
- Business/KI-Seite: **Sie** ist dort in Ordnung, aber dann durchgehend.
- Impressum, Datenschutz, Erstinformation und AGB dürfen beim förmlichen „Sie“ bleiben.

### 10. 404-Seite 💻

Probleme: kein Menü, kein Footer, Seitentitel identisch mit der Startseite, „Sie“-Form.

```tsx
// app/not-found.tsx
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Seite nicht gefunden | TarifWerk",
  robots: { index: false },
};

export default function NotFound() {
  return (
    <main id="inhalt" className="...">
      <p className="...">404</p>
      <h1>Diese Seite gibt es nicht. Klarheit schon.</h1>
      <p>Kein Drama. Starte auf der Startseite oder schau direkt hier:</p>
      <nav aria-label="Beliebte Seiten">
        <Link href="/anfrage">Vertrag prüfen lassen</Link>
        <Link href="/leistungen">Leistungen</Link>
        <Link href="/rechner">Kostenrechner</Link>
        <Link href="/kontakt">Kontakt</Link>
      </nav>
    </main>
  );
}
```

Header und Footer kommen automatisch dazu, wenn `not-found.tsx` im Layout liegt, das auch Header/Footer rendert. Heute rendert die 404 offenbar außerhalb davon.

### 11. Server-Antwortzeit 💻

**Messung:** HTML-Antwort nach 0,55–1,15 s, `cache-control: private, no-store` auf allen Seiten.

**Ursache (sehr wahrscheinlich):** Die CSP arbeitet mit einem **Nonce pro Anfrage** (`script-src 'nonce-…' 'strict-dynamic'`). Next.js muss dafür jede Seite bei jedem Aufruf neu rendern, das CDN kann nichts zwischenspeichern.

**Optionen:**
1. **Hash-basierte CSP statt Nonce:** `experimental.sri` in `next.config` (Subresource Integrity) erlaubt statisch erzeugte Seiten mit strenger CSP. Vorher prüfen, ob es mit eurem Build (Turbopack/Webpack) und eurer Next-Version funktioniert.
2. **Nonce nur dort, wo nötig:** CSP mit Nonce nur für `/portal` und `/api`, die öffentlichen Marketing-Seiten statisch mit `script-src 'self'` plus Hashes.
3. Danach für öffentliche Seiten `export const revalidate = 3600;` (ISR).

Ziel: HTML-Antwort unter 200 ms.

### 12. Gründerfoto zu groß 💻

`/api/advisors/1/image` liefert ein **1200 × 1200 px**-WebP (77 KB), angezeigt wird es als 56-px-Kreis. Lösung: über `next/image` mit `sizes="56px"` ausliefern oder in der API mit `sharp` auf die angefragte Breite skalieren:

```ts
// in der Route /api/advisors/[id]/image
const w = Math.min(Number(searchParams.get("w")) || 256, 800);
const buf = await sharp(original).resize(w, w, { fit: "cover" }).webp({ quality: 80 }).toBuffer();
```

und im Code `?w=112` (2× für Retina) anfragen. Ergebnis: etwa 4 KB statt 77 KB.

---

## 🟡 Feinschliff

### 13. Weiterleitung 💻 / Firebase

Heute: `http://tarifwerk.eu` → 301 → `https://tarifwerk.eu` → **302** → `https://www.tarifwerk.eu`. Ziel: ein einziger **301** direkt auf `https://www.tarifwerk.eu`.

Die 302 kommt von der Plattform (Firebase App Hosting). In der Firebase Console unter **App Hosting → Domains** prüfen, wie `tarifwerk.eu` eingerichtet ist. Falls dort kein dauerhafter Redirect möglich ist: `tarifwerk.eu` als normale Domain verbinden und in Next umleiten:

```js
// next.config.(js|ts)
async redirects() {
  return [
    {
      source: "/:path*",
      has: [{ type: "host", value: "tarifwerk.eu" }],
      destination: "https://www.tarifwerk.eu/:path*",
      permanent: true,
    },
  ];
}
```

### 14. Mehr Inhalte für Google 👤 + 💻

Heute gibt es 3 Ratgeber-Artikel und 3 Städteseiten. Themenvorschläge für die nächsten Artikel (je 800–1.500 Wörter, mit Quellen wie bisher):

1. Strompreiserhöhung bekommen – was jetzt tun?
2. Gasvertrag kündigen: Fristen und Sonderkündigungsrecht
3. Glasfaser-Vertrag: worauf vor der Unterschrift achten
4. Glasfaser in Wiesbaden: Verfügbarkeit prüfen
5. Handyvertrag ohne Handy oder mit Handy – was ist günstiger?
6. Umzug: Strom, Gas und Internet richtig ummelden
7. Wärmepumpe: Förderung und Stromtarif
8. Balkonkraftwerk: lohnt sich das?
9. PV-Speicher nachrüsten: Rechnung und Fallstricke
10. Dynamischer Stromtarif: für wen sinnvoll?
11. Abschlag zu hoch? Strom- und Gasabschlag anpassen
12. Internet zu langsam: Rechte nach § 57 TKG (Minderung)
13. Haftpflicht, Hausrat & Co.: welche Versicherungen wirklich wichtig sind (mit Fachpartner)
14. Alarmanlage oder Kamera: was Versicherer erwarten
15. Gold kaufen: Kosten und Risiken verständlich erklärt

Städteseiten nur für Orte, in denen wirklich ein Berater sitzt (München, Wolfsburg laut Profilen). Keine Copy-Paste-Seiten.

### 15. Sitemap 💻

Alle URLs haben `lastmod 2026-10-30`. Pro Seite das echte Änderungsdatum eintragen (z. B. aus dem Datum im Artikel oder dem Datensatz). `changefreq` und `priority` ignoriert Google, die können weg.

### 16. Permissions-Policy 💻

`bluetooth=()` kennt der Browser nicht und meldet bei jedem Aufruf einen Fehler in der Konsole. Aus dem Header streichen:

```
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), serial=()
```

### 17. Google-Bewertungen 👤

Heute 28 Bewertungen mit 4,9. Ziel: 100+.
- Nach jeder Beratung per WhatsApp einen Direktlink zur Bewertung schicken (Google Business Profile → „Rezensionen erhalten“ → Link kopieren).
- QR-Code auf Visitenkarte und Flyer.
- Auf jede Bewertung kurz antworten.
- Keine Gegenleistung für Bewertungen anbieten (verboten).

### 18. Formular-Abstand 💻

Auf `/anfrage` stoßen unten der Hinweis „So verdienen wir…“ und der Button „Weiter zum Kontakt“ fast aneinander. Hinweis über den Button setzen oder `gap-4` zwischen Text und Button.

---

## Code freigeben

Damit Claude die 💻-Punkte direkt umsetzen kann, gibt es zwei Wege:

**A) Das bestehende Repo freigeben (empfohlen)**
1. In der Firebase Console unter **App Hosting → Backend (laut Server-Header vermutlich „neuuuuuuutarif1509“) → Einstellungen** nachsehen, welches GitHub-Repo verbunden ist.
2. Unter https://github.com/apps/claude/installations/select_target die Claude-App für dieses Repo (bzw. dessen Konto oder Organisation) freigeben.
3. In einer neuen Claude-Sitzung dieses Repo auswählen.

**B) Code in dieses Repo schieben**
Den Projektordner (ohne `node_modules`, `.next` und `.env`-Dateien!) nach `pyn7r68zsg-lgtm/TarifWerk` pushen. Achtung: Dieses Repo ist **öffentlich**. Für den Webseiten-Code besser auf „privat“ stellen.
