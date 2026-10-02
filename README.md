# Clarity — support & legal site

Static pages served via GitHub Pages (`https://saynfeld.github.io/clarity/`).

| App Store Connect field | Page |
|---|---|
| Support URL | `index.html` |
| Privacy Policy URL | `privacy.html` |
| Terms of Service (linked from the app's Settings and the description) | `terms.html` |

All pages are bilingual (English first, Russian below, anchors `#en` / `#ru`),
share `style.css` and follow the system light/dark theme. The title is
monospaced, the body is a serif face, defined terms are bold and underlined,
and the revision date closes each document.

The legal entity is **Matchy Labs Ltd**, England and Wales, company number
17479437, registered office 71-75 Shelton Street, Covent Garden, London,
WC2H 9JQ, United Kingdom; company email hello@matchylabs.xyz. Unfilled values in
the sources (`[[...]]`) render as `<span class="placeholder">` — search for
`placeholder` before publishing.

`privacy.html` and `terms.html` are generated: the texts live in the app
(`../../App/NetStatus/Legal/{privacy,terms}.{en,ru}.md`, shown in-app in the
device language). After editing them run `python3 build_legal.py` here and
commit both repos. `index.html` and `style.css` are edited directly.
