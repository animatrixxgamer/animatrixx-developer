# Animatrixx Developer

One-page portfolio for Animatrixx Developer — a solo software studio in Ondo, Nigeria building
websites, web apps and Python automation for small businesses and schools.

**Live:** https://animatrixxgamer.github.io/animatrixx-developer/

Plain HTML, CSS and JavaScript. No build step, no framework, no dependencies to install — the files
in this repository are the site.

## Running it locally

Open `index.html` in a browser, or serve the folder so relative paths and the `/og-image.png`
preview resolve the same way they do in production:

```bash
python3 -m http.server 3000
# then visit http://localhost:3000
```

## Files

| File | What it is |
|---|---|
| `index.html` | The whole page: hero, about, work, services, contact form. All copy lives here. |
| `styles.css` | All styles. Design tokens (colours, spacing, radii) are at the top of the file. |
| `main.js` | Mobile nav, scroll reveals, active nav link, the WhatsApp contact form, footer year. |
| `fonts/` | Self-hosted latin-subset variable fonts: Inter (100–900) and Space Grotesk (300–700). |
| `og-image.png` | 1200×630 social preview card, shown when a link is shared. |
| `_config.yml` | GitHub Pages (Jekyll) config; excludes the repo notes from the published site. |
| `.vercelignore` | Keeps the repo notes out of Vercel deployments. |
| `positioning.md` | Internal positioning and client-message notes. Gitignored, local only, not part of the site. |
| `tools/downscale.py` | Stdlib-only PNG downscaler. Regenerates `og-image.png` from a 2× screenshot. |

## Editing

- **Copy** is written directly in `index.html`. Keep it consistent with `positioning.md` — it is the
  source of truth for tone and claims.
- **Colours and spacing** are CSS custom properties at the top of `styles.css`; changing them there
  updates the whole page.
- **The WhatsApp number** is set once, in `main.js` (`WHATSAPP`, digits only including country code).
  The `wa.me` links in `index.html` need the same number.
- **The social card** (`og-image.png`) is referenced host-relative (`/og-image.png`), so it resolves
  from whatever domain serves the page. Replace the file, keep the 1200×630 size.
- **Fonts** are the files in `fonts/`, declared with `@font-face` at the top of `styles.css` — nothing
  is fetched from Google at runtime. If you swap a font file, re-measure the fallback overrides in
  that block: `size-adjust` and the ascent/descent overrides are matched to the real font metrics so
  the fallback swap does not shift layout.

## Deployment

`main` is published by GitHub Pages, which serves the site directly from the repository root. Push to
`main` and it redeploys on its own.

`index.html` sets `<link rel="canonical">` and `og:url` to the Pages URL as the one canonical address
for the site. If this moves to a custom domain or to Vercel as the primary host, update those two
lines together so search engines and shared links agree.

## Notes

`positioning.md` is working notes, not site content. It is gitignored and exists only in local
checkouts, so it is never published and no longer readable on GitHub (older commits still contain
it). The Pages build and `.vercelignore` also exclude it as a second line of defence.

`audit/` holds local audit screenshots and image captures. It is gitignored — the files are
regenerable and never belong in the repository.
