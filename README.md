# Vantage Risk Solutions — website

A five-page website for the **brokerage's services** — employee benefits and commercial property
& casualty. It is not the client portal, and it never mentions software.

**The copy here is a draft.** Stephanie and Rebecca own the wording (2026-09-29 meeting, §3.6).
The service lists are written so an AI research tool can read, from the page itself, exactly what
the firm does — that is the reason the site was commissioned.

No build step. No JavaScript. Nothing fetched from anywhere — no fonts, scripts, analytics or
images. Double-click `index.html` and it opens in your browser; it works the same on any host.

## Pages

| File | What it holds |
|---|---|
| `index.html` | Home — the two practices, how we work, industries |
| `employee-benefits.html` | Every benefits line, the three funding models, group sizes, what we do, year-round service |
| `property-casualty.html` | Every P&C line, what we do, year-round service |
| `about.html` | Who we are, referral partners, the questions we get, **and all the contact details** |
| `legal.html` | Licensing, coverage, compensation, privacy |

The detail lives on the two practice pages, the way alliant.com does it; the home page carries
only what a first-time visitor needs. Home is **274 words** against 2,547 on the old single page,
and no page exceeds ~620.

## Files

```
index.html · employee-benefits.html · property-casualty.html · about.html · legal.html
styles.css                     one stylesheet, shared by all five pages
images/hero.webp               home hero — an office building
images/benefits.webp           Employee Benefits
images/pc.webp                 Commercial Property & Casualty
images/about.webp              About
images/hero.svg                our own drawing, kept as a fallback
images/CREDITS.md              where each photograph came from
images/vantage-silver-v/       the silver V logo kit — the logo the site uses:
  index.html                   the kit's own page: every file, with usage rules
  vantage-logo.svg|.png        gunmetal logo, for white or light backgrounds
  vantage-logo-white.*         silver logo — what the navy header and footer use
  vantage-logo-stacked*.*      stacked logo, for tall spaces
  vantage-mark*.svg|.png       mark only, gunmetal and silver
  vantage-app-icon.*           512px app icon, for social profile pictures
  favicon.svg · favicon-32.png · apple-touch-icon.png
images/lighthouse-logo/        the lighthouse logo kit, kept as the alternative; its own
                               page is brand-kit.html
```

The two kit pages (`images/vantage-silver-v/index.html`, `images/lighthouse-logo/brand-kit.html`)
are internal reference — nothing links to them, and you can delete them before publishing.

## Changing a sentence

1. Open the page in a plain-text editor — **Notepad** on Windows or **TextEdit** on a Mac
   (in TextEdit choose Format → Make Plain Text first). Not Word.
2. Use Find (Ctrl+F / Cmd+F) to search for a few words of the sentence.
3. Change only the words **between** a closing `>` and the next opening `<`. Everything inside
   the angle brackets is the page's structure — leave it alone.
4. Type an ampersand as `&amp;` (the files already do this: `Property &amp; Casualty`).
5. Save, then refresh the browser tab.
6. A line of business is one `<li>…</li>` line. Add or remove a line by adding or removing one.

If the layout breaks or stray brackets appear, undo and retype rather than guess.

> **The one thing to watch:** the navy bar at the top and the footer at the bottom are **copied
> into all five pages**. There is no build step, which is what keeps the site dependency-free, so
> changing a nav link or the footer means making the same edit in all five files. Everything else
> is per page.

## Before this can be published — the placeholder checklist

Every fact the firm still has to supply is wrapped in `<span class="ph">[LIKE THIS]</span>` and
renders with an **amber dashed outline**, so nothing fake can ship quietly. Filling one in means
deleting the whole span — from `<span` to `</span>` — and typing the value in its place.

They are deliberately gathered on **two pages only**, so there is one short round of filling in:

| Placeholder | Page | Who supplies it |
|---|---|---|
| `[CITY, STATE]` | `about.html` (twice) | Joey / Stephanie |
| `[SERVICE AREA]` | `about.html` | Stephanie. The record's "all 50 states" (2026-08-19) is the **benefits** side only; the P&C footprint is unstated — if the two differ, the About sentence has to name them separately |
| `[LEADERSHIP — …]` | `about.html` | Each person's consent before a name or photo appears |
| `[CONFIRM THIS OFFER WITH JOEY …]` | `about.html` › Referral partners | Joey — delete the paragraph if the offer is not public |
| `[PERSONAL LINES — …]` | `about.html` › Questions | Joey / Nick — say whether the firm writes personal auto or homeowners |
| `[STATES LICENSED]` | `about.html`, `legal.html` | Joey (~30 reciprocal states as of 2026-08-19; confirm) |
| `[FIRM PHONE]`, `[FIRM EMAIL]` | `about.html` › Contact; `[FIRM EMAIL]` again on `legal.html` | Stephanie. Once filled, wrap them in `<a href="tel:…">` / `<a href="mailto:…">` — a note in the HTML shows where |
| `[STREET ADDRESS, CITY, STATE ZIP]`, `[OFFICE HOURS]` | `about.html` › Contact | Stephanie |
| `[LEGAL ENTITY NAME]` | `legal.html` (twice) | Joey |
| `[LICENSE NUMBER]` | `legal.html` | Joey |
| `[PRIVACY NOTICE — counsel to supply]` | `legal.html` | Counsel |

**The publish check:** open each of the five pages and make sure **no amber dashed boxes are
left**. That is the entire test. (For whoever publishes: `grep -n "\[" *.html` must return nothing.)

## Confirm before publishing — things deliberately left off or left plain

- **"Independent."** The word does not appear anywhere. Until the January 1, 2027 structure
  exists, a research tool reading staff LinkedIn pages would find Brown & Brown / Risk Strategies
  and call the site inconsistent. Revisit after January 1.
- **Multiple pages.** Joey asked for one scrolling page and said twice that he does not want
  dropdowns. The site now has five pages — but **the nav is flat, one link per page, with no
  dropdown anywhere**, and each page still scrolls as one. Worth telling him before he sees it.
- **Lines not listed** because they are unconfirmed on a public page: Realtor E&O and Technology
  E&O (ask **Sonia** — the 2026-09-17 P&C call left open which professions she actually writes),
  pharmacy benefit management / PBM (ask Stephanie), individual life (a referral product, not an
  employer line).
- **Industries.** The seven **headings** trace to accounts in the firm's own records. The one-line
  descriptions are generic wording and need Stephanie's and Nick's pass. Never name a client —
  not even a generic phrase that happens to be a client's name.
- **Claims and inspections** (P&C, "Between renewals") are worded from Sonia's description on
  2026-06-22; she should read those two lines.
- **Every paragraph on `legal.html`** is a draft for counsel.
- **Nothing on the site is a number** (years in business, clients, lives, carriers) because none
  is confirmed. Add figures only when they are real.

## Photography

Four photographs, all **Unsplash License** — commercial use, no attribution required. Every one
was chosen with **no recognizable face, no logo and no legible text** in frame, because neither
the Unsplash nor the Pexels licence covers model releases or trademarks; a faceless photo avoids
the question entirely, and avoids a stock face reading as one of our clients or staff.
`images/CREDITS.md` records the photographer, the source page and the date for each.

To swap one: replace the file, keep the name, and update `CREDITS.md`. Landscape 3:2, at least
2400 × 1600, saved as WebP. **Never upscale a small image** — that is what makes a site look
blurry, and it is the exact fault the team flagged on a competitor's site.

## Using the logo

The site uses the **silver V** (`images/vantage-silver-v/`). From the kit's own guidance
(`images/vantage-silver-v/index.html`):

- **Size** — 32–48px tall in a header. Never below 24px. The site uses 34px in the header and
  30px in the footer.
- **Clear space** — at least the height of the triangle inside the V around it.
- **Backgrounds** — gunmetal on white or light grey, the silver version on dark. The header and
  footer are navy, so both use the silver version (`vantage-logo-white.svg`).
- **Don't** stretch it, recolour it, add effects, or rearrange the V and the name.
- **Site colours** are still the lighthouse kit's, kept on purpose while the logo is being
  chosen: Navy `#173a63` · Blue `#2e6fc7` · Cyan `#22b8d8` · Violet `#6d4bb6` · Beacon `#f5b82e`.
  Cyan is used for small rules only — as type it is too pale to read. The silver kit's own
  palette (Ink `#16181c`, Gunmetal `#2b323c`, Steel `#7c848e`, Silver `#c4c9cf`) is not used yet.
- The wordmark is IBM Plex Sans SemiBold converted to vector shapes, so it needs no font installed.

**To switch back to the lighthouse:** in all five pages, replace `images/vantage-silver-v/` with
`images/lighthouse-logo/`, and on the two `brand-logo` images change `width="180" height="44"` to
`width="217" height="52"`.

The logo reads **Vantage**; the full legal name appears on the About page, on `legal.html` and in
the logo's alt text, which is what a screen reader and a search engine read.

*(Note on the lighthouse files as they arrived 2026-09-29: every `.svg` in the drop was actually a PNG and
every `.png` an SVG, and the names did not match the artwork. They were renamed to match what
each file really contains, checked against `brand-kit.html`. The file named `favicon-32.png` was
really the 180px phone icon, so it is now `apple-touch-icon.png` and a true 32px favicon was
generated. One kit file was never in the drop: `vantage-mark.svg`, the full-colour mark as an
SVG — the PNG of it is here, and `favicon.svg` is the same artwork. Nothing needs it.)*

## Design

The layout follows **alliant.com**, which the firm named as the reference: three surfaces (white,
one grey tint, one navy band), square corners throughout, large headings at regular weight with
small heavy labels above them, generous spacing, and **photographs shown clean with nothing laid
over them** — text sits on a solid panel beside the photo, never on top of it. Body type is 18px.
Deliberately not copied: Alliant's rotating seven-slide hero, its awards strip, and its statistics
strip (which would need numbers the firm cannot yet prove).

## Fonts

The stylesheet asks for IBM Plex Sans (the brand font) and falls back to the system font, so the
page never fetches a font. To ship Plex itself: download the OFL `.woff2` files (400/500/600/700)
into a `fonts/` folder and paste this at the top of `styles.css`, once per weight:

```css
@font-face { font-family: 'IBM Plex Sans'; font-weight: 400; font-style: normal;
             src: url('fonts/IBMPlexSans-Regular.woff2') format('woff2'); font-display: swap; }
```

## Publishing

Any static host works because there is nothing to build.

- **GitHub Pages:** put this folder at the root of its own repository → Settings → Pages →
  "Deploy from a branch" → `main` / root. For a custom domain add a `CNAME` file containing the
  domain and point DNS at GitHub Pages. (The domain — `vantageer.com` vs `vantagerisk.com` — was
  unconfirmed on 2026-09-29.)
- **Netlify / Cloudflare Pages:** drag the folder in.

Every change is a commit, so a bad edit is one revert away — that is the reason the site lives in
version control instead of with a third party.

## Later, if wanted

- A `schema.org` `InsuranceAgency` block — only once every placeholder is filled; one containing
  `[FIRM PHONE]` is worse than none.
- A contact form (needs a form endpoint; a static site has none).
- A news / insights page, once there are three real articles.
