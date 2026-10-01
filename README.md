# Vantage Risk Solutions — website

A website for the **brokerage's services** — employee benefits and commercial property & casualty —
in two layouts: **five pages** (the default) and the same words on **one scrolling page**
(`one-page.html`), chosen with the **Multi-page | One-page** switch beside the logo. It is not the
client portal, and it never mentions software.

**The copy here is a draft.** Stephanie and Rebecca own the wording (2026-09-29 meeting, §3.6).
The service lists are written so an AI research tool can read, from the page itself, exactly what
the firm does — that is the reason the site was commissioned.

No build step. No JavaScript. Nothing fetched from any other server — no scripts, analytics or
outside images. The site's typeface ships with it, in `fonts/`. Double-click `index.html` and it
opens in your browser; it works the same on any host.

## Pages

| File | What it holds |
|---|---|
| `index.html` | Home — the two practices, how we work, industries |
| `employee-benefits.html` | Every benefits line, the three funding models, group sizes, what we do, year-round service |
| `property-casualty.html` | Every P&C line, what we do, year-round service |
| `about.html` | Who we are, referral partners, the questions we get, **and all the contact details** |
| `legal.html` | Licensing, coverage, compensation, privacy |
| `one-page.html` | Everything above on one scrolling page — a hand-made copy of the five pages (see **The two layouts**) |

The detail lives on the two practice pages; the home page carries only what a first-time visitor
needs. Home is **250 words**, and none of the five pages exceeds ~590. `one-page.html` carries all
of it — about 1,830 words — for visitors who would rather scroll.

## Files

```
index.html · employee-benefits.html · property-casualty.html · about.html · legal.html · one-page.html
styles.css                     one stylesheet, shared by all six pages
fonts/                         IBM Plex, SIL Open Font License (OFL.txt): six .woff2 files —
                               IBMPlexSerif-Light-Latin1, IBMPlexSerif-LightItalic-Latin1,
                               IBMPlexSans-Regular-Latin1, IBMPlexSans-SemiBold-Latin1,
                               IBMPlexSans-SemiBold-Pi, IBMPlexMono-Medium-Latin1
_tools/check_one_page.py       checks one-page.html still matches the five pages, and that every
                               font file the stylesheet names exists (reads only; GitHub Pages
                               does not publish _tools/)
images/hero.webp               home hero — a glass tower against a blue sky
images/benefits.webp           Employee Benefits — a bright atrium with trees
images/pc.webp                 Commercial Property & Casualty — a clinic waiting area
images/about.webp              About — a sunlit office with plants
images/hero.svg                our own drawing, kept as a fallback
images/CREDITS.md              where each photograph came from
images/vantage-silver-v/       the silver V logo kit — the logo the site uses:
  index.html                   the kit's own page: every file, with usage rules
  vantage-logo.svg|.png        gunmetal logo, for white or light backgrounds
  vantage-logo-white.*         silver logo — what the dark header and footer use
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
7. **Change the five pages only — never `one-page.html`.** Every sentence on it is a copy of one on
   the five pages; Daniel copies your change across, and runs the checker, before publishing.

Three layout rules to keep while editing:

- In **Questions we get** (About) and on the Disclosures page, each question is one `<h3>` followed
  by exactly one `<p>`. Put any extra sentence inside that same `<p>`; a second paragraph shifts the
  two-column layout.
- Never put a link inside a line-of-business `<li>`: that list trims its own left edge, and a link
  there would be clipped.
- In the home headline, `<em>…</em>` marks the phrase set in silver italics. Keep it identical in
  `index.html` and `one-page.html`.

If the layout breaks or stray brackets appear, undo and retype rather than guess.

> **The two things to watch:** (1) the dark bar at the top and the footer at the bottom are
> **copied into all six pages** — on `one-page.html` their links point at sections instead of
> files; (2) **every sentence on the five pages is also in `one-page.html`**. There is no build
> step, which is what keeps the site dependency-free, so both are copying jobs — Daniel's, at
> publish time. `python _tools/check_one_page.py` lists anything that no longer matches.

## The two layouts

Every page has a **Multi-page | One-page** switch beside the logo: one plain link to the other
layout, beside a label marking the one you are on. There is no script:

- **One-page** opens `one-page.html` at the chapter for the page you were on — from Employee
  Benefits, the Employee Benefits chapter. **Multi-page** goes back to Home.
- The choice is not remembered between visits (that would need a script), but every link inside a
  layout stays inside it.

`one-page.html` is the five pages one after another — Home, Employee Benefits, Commercial P&C,
About, Disclosures — with the same words, photos and look. It is a **copy**; the five pages are the
master. These are the only deliberate differences, and the checker allows exactly these (it does
not compare comments, or each page's own title and description):

1. The dark **Talk to a broker** band at the bottom of Home, Employee Benefits and P&C is left out —
   the page already has the full Contact section from About, just before Disclosures.
2. Each page's main heading becomes a chapter heading (`<h2 class="chapter-title">`, same size), so
   the page has one main heading: Home's.
3. Each chapter's first section carries its id (`employee-benefits`, `property-casualty`, `about`,
   `legal`) and the class `chapter`; `<body>` carries `id="top"`.
4. The three chapter photos load lazily.
5. Links point at sections of the page: `X.html` becomes `#` and X's chapter, `X.html#part` becomes
   `#part`, and Home is `#top`. `tel:`, `mailto:` and web links stay as they are.
6. Its own title and description.
7. The footer column is headed **Sections**, not Pages.
8. The switch is reversed: **Multi-page** is the one link to `index.html`.
9. No nav link is marked as the current page.
10. Its own comments.

Each chapter opens on its dark hero (Disclosures on its off-white title band, straight after the
dark Contact section), so no rule is drawn between chapters; printing still starts each chapter on a
new page.

**Keeping it in step (Daniel, at publish time).** After any change to the five pages — a filled
placeholder too — copy the same change into `one-page.html` (Find a few words; the text is
identical), then run:

    python _tools/check_one_page.py

It prints `OK` when the two match. Otherwise it lists what differs — the first difference in each
section — with the line number in both files; fix those and run it again. It changes nothing. If it
flags differences on two publishes in a row, it is time to generate `one-page.html` instead of
copying by hand — the checker already holds what a generator needs.

**Keeping only one layout.** To keep the five pages: delete `one-page.html` and `_tools/`, take the
switch out of the five pages and its rules out of `styles.css` — but keep the two header fixes
marked in the 1100px block — and change the NAV and FOOTER comments back to five pages. To keep the
one page: move its content into `index.html` and turn the other pages into redirects to their
chapters.

## Before this can be published — the placeholder checklist

Every fact the firm still has to supply is wrapped in `<span class="ph">[LIKE THIS]</span>` and
renders with an **amber dashed outline**, so nothing fake can ship quietly. Filling one in means
deleting the whole span — from `<span` to `</span>` — and typing the value in its place.

They are deliberately gathered in **`about.html` and `legal.html`** (and repeated in
`one-page.html`), so there is one short round of filling in. Fill them on the two pages; Daniel
copies each value into `one-page.html`, and the checker lists any he misses.

| Placeholder | Page | Who supplies it |
|---|---|---|
| `[CITY, STATE]` | `about.html` (twice), `one-page.html` (twice) | Joey / Stephanie |
| `[SERVICE AREA]` | `about.html`, `one-page.html` | Stephanie. The record's "all 50 states" (2026-08-19) is the **benefits** side only; the P&C footprint is unstated — if the two differ, the About sentence has to name them separately |
| `[LEADERSHIP — …]` | `about.html`, `one-page.html` | Each person's consent before a name or photo appears |
| `[CONFIRM THIS OFFER WITH JOEY …]` | `about.html` › Referral partners, `one-page.html` | Joey — delete the paragraph if the offer is not public |
| `[PERSONAL LINES — …]` | `about.html` › Questions, `one-page.html` | Joey / Nick — say whether the firm writes personal auto or homeowners |
| `[STATES LICENSED]` | `about.html`, `legal.html`, `one-page.html` (twice) | Joey (~30 reciprocal states as of 2026-08-19; confirm) |
| `[FIRM PHONE]`, `[FIRM EMAIL]` | `about.html` › Contact; `[FIRM EMAIL]` again on `legal.html`; the same in `one-page.html` | Stephanie. Once filled, wrap them in `<a href="tel:…">` / `<a href="mailto:…">` — a note in the HTML shows where |
| `[STREET ADDRESS, CITY, STATE ZIP]`, `[OFFICE HOURS]` | `about.html` › Contact, `one-page.html` | Stephanie |
| `[LEGAL ENTITY NAME]` | `legal.html` (twice), `one-page.html` (twice) | Joey |
| `[LICENSE NUMBER]` | `legal.html`, `one-page.html` | Joey |
| `[PRIVACY NOTICE — counsel to supply]` | `legal.html`, `one-page.html` | Counsel |

**The publish check:** open each of the **six** pages and make sure **no amber dashed boxes are
left**. That is the entire test. (For whoever publishes: `grep -n "\[" *.html` must return nothing,
and `python _tools/check_one_page.py` must print `OK`.)

## Confirm before publishing — things deliberately left off or left plain

- **"Independent."** The word does not appear on any page. Until the January 1, 2027 structure
  exists, a research tool reading staff LinkedIn pages would find Brown & Brown / Risk Strategies
  and call the site inconsistent. Revisit after January 1.
- **One page or several.** Joey asked for one scrolling page and said twice that he does not want
  dropdowns. Both now exist: five pages by default, and the same words on one scrolling page, one
  click away on the **Multi-page | One-page** switch beside the logo. The nav is still flat — one
  link per page, no dropdown anywhere. Show him the switch.
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
blurry, and it is the exact fault the team flagged on a competitor's site. Each photo's crop in the
tall hero cell is set by file name in `styles.css` (`object-position`, in the Hero block); after a
swap, check the new picture both in the hero and in its 16:10 card on the home page.

## Using the logo

The site uses the **silver V** (`images/vantage-silver-v/`). From the kit's own guidance
(`images/vantage-silver-v/index.html`):

- **Size** — 32–48px tall in a header. Never below 24px. The site uses 34px in the header and
  30px in the footer.
- **Clear space** — at least the height of the triangle inside the V around it.
- **Backgrounds** — gunmetal on white or light grey, the silver version on dark. The header and
  footer are midnight `#08121e` — the kit's near-black in darkness, the brand navy in hue — so both
  use the silver version (`vantage-logo-white.svg`).
- **Don't** stretch it, recolour it, add effects, or rearrange the V and the name.
- **Site colours:** midnight `#0c1a2b` (heroes, the contact band) and `#08121e` (bar, footer);
  off-white paper `#f5f4f0` and white for content; ink `#0c1a2b` for headings; link blue `#235eb0`;
  cyan `#22b8d8` for the small rules and marks on light surfaces and for labels on dark ones, with
  the darker `#16607a` where the cyan family is used as small type on light. Navy `#173a63` remains
  only as the glow in the contact band. The lighthouse kit's other colours are kept in the
  stylesheet for the kit and are not used.
- The wordmark is IBM Plex Sans SemiBold converted to vector shapes, so it needs no font installed.

**To switch back to the lighthouse:** in all six pages, replace `images/vantage-silver-v/` with
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

The look is **Editorial Midnight**: three dark frames on every page — the opening panel, the
**Talk to a broker** band and the footer — under a darker top bar, with white and off-white content
between them. Square corners throughout; structure comes from ruled rows and thin hairlines, not
cards, shadows or icons. Statements are set in IBM Plex Serif Light at 28px and up, everything a
visitor reads or clicks in IBM Plex Sans, and the small labels and step numbers in IBM Plex Mono.
One accent, cyan, appears as small marks on light surfaces and as labels on dark ones. Photographs
are shown clean, in full colour, beside a solid panel — never darkened, never with text on top —
and the only motion is a photo that settles on load and a label bar that grows, both off when the
visitor's system asks for reduced motion. Nothing that carries text ever starts hidden.

The fact lists are set so they scan like a catalogue: the lines of business as ruled rows with the
group label beside them, the service steps in two numbered columns, and the questions and the
disclosures as two-column ledgers with every answer visible. Deliberately left out: carousels,
statistics and award strips, logo walls, faces, and anything that looks like software.

## Fonts

IBM Plex is the brand typeface (the wordmark is Plex Sans SemiBold). The site ships it from
`fonts/` — six `.woff2` files, about 118 KB on the home page and 85–93 KB on the others — so the
pages render the same everywhere and still request nothing from any other server:

| File | Used for |
|---|---|
| `IBMPlexSerif-Light-Latin1.woff2` | statements: page and section headings |
| `IBMPlexSerif-LightItalic-Latin1.woff2` | the silver italic phrase in the home headline (home and one-page only) |
| `IBMPlexSans-Regular-Latin1.woff2` | everything a visitor reads |
| `IBMPlexSans-SemiBold-Latin1.woff2` | bold lead-ins, buttons, names, questions |
| `IBMPlexSans-SemiBold-Pi.woff2` | only the → on links and the ✓ in check lists |
| `IBMPlexMono-Medium-Latin1.woff2` | the small labels and step numbers |

The files are the Latin-1 subsets from IBM's own packages (`@ibm/plex-serif` 2.0.0,
`@ibm/plex-sans` 1.1.0, `@ibm/plex-mono` 2.5.0, folder `fonts/split/woff2/`, also in the releases
at github.com/IBM/plex), under the SIL Open Font License — the licence text is `fonts/OFL.txt`.
To add a weight, download its `…-Latin1.woff2`, copy one `@font-face` block at the top of
`styles.css`, and keep the file name's exact case: the web host is case-sensitive, Windows is not,
and `python _tools/check_one_page.py` checks every font path for that reason. There is no
`<link rel="preload">` on purpose — the checker does not compare one across the six heads, and
opening a page by double-click dislikes it. While the serif loads on a first visit the headlines
show in Georgia, sized to match, so nothing jumps.

## Publishing

Any static host works because there is nothing to build.

- **GitHub Pages:** put this folder at the root of its own repository → Settings → Pages →
  "Deploy from a branch" → `main` / root. For a custom domain add a `CNAME` file containing the
  domain and point DNS at GitHub Pages. (The domain — `vantageer.com` vs `vantagerisk.com` — was
  unconfirmed on 2026-09-29.) GitHub Pages runs Jekyll on the folder, which skips names starting
  with `_`, so `_tools/` is not published. Don't add a `.nojekyll` file — it would publish `_tools/`.
- **Netlify / Cloudflare Pages:** drag the folder in, leaving `_tools/` out.
- After a publish, open the site once with the browser's developer tools on the Network tab and
  confirm every `fonts/*.woff2` file returns 200. If one is 404, its name differs in case from the
  stylesheet.

Every change is a commit, so a bad edit is one revert away — that is the reason the site lives in
version control instead of with a third party.

## Later, if wanted

- A `schema.org` `InsuranceAgency` block — only once every placeholder is filled; one containing
  `[FIRM PHONE]` is worse than none.
- A contact form (needs a form endpoint; a static site has none).
- A news / insights page, once there are three real articles.
- Smaller copies of the photos for phones (`srcset`): every attribute added must be mirrored in
  `one-page.html`, so it was left out of the first build.
