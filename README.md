# quarto-slides-starter

A starting point for Quarto RevealJS slide decks that fullscreen correctly,
print correctly, and stay that way. The settings in `deck.qmd` were
established by debugging real decks; the rules below are why they work.

This README is written to be followed by a human or by an AI assistant
working on a deck. Treat the rules as constraints, not suggestions.

## Quick start

1. Create a repo from this template (green "Use this template" button, or
   `gh repo create my-deck --template Alandougherty/quarto-slides-starter`).
2. Edit `deck.qmd`. Preview with:
   `quarto preview deck.qmd --port 4200 --no-browser`
   (add `--host 0.0.0.0` to view from another machine on your network).
3. Export to PDF with `./export.sh <url> <out.pdf>` (decktape; recommended;
   run it with the preview from step 2 still serving).

The repo root is a standard Quarto project (`_quarto.yml` beside
`deck.qmd`), the same shape as the example, so everything said about the
example's structure applies to your deck too. `quarto render` with no
filename renders just `deck.qmd`; the examples are their own projects
with their own `_quarto.yml`. Project form matters once a deck has
executable code: `freeze` (cached code results, already configured) is
honoured only by project renders.

## Delivering the deck

When it is time to actually present, render (Quarto's word for export) the
deck as ONE self-contained HTML file:

    quarto render -M embed-resources:true

Note the command names no file: a project render respects the render list
in `_quarto.yml` (only `deck.qmd`) and keeps `freeze` honoured once the
deck gains executable code (rule 7).

This inlines every stylesheet, script, image and video into a single
`.html` you can put on a USB stick, email, or open on the venue machine
with no internet, no Quarto install, and no `_files/` folder to forget.
Without it, the rendered html silently depends on its sibling `*_files/`
directory, and a copied-alone file breaks at the podium. For day-to-day
preview keep it off (faster renders) and add the `-M` flag only for the
delivery build.

Two documented caveats: math libraries are not embedded by default (add
`self-contained-math: true` if the deck uses math), and the Chalkboard
plugin is incompatible with `embed-resources`. `self-contained` is the
deprecated old name for the same option.

## Suggested tools

| Tool | Why | Install (macOS) |
|---|---|---|
| Quarto | renders and previews the deck | `brew install --cask quarto` |
| Node.js | runs decktape via `npx` (no separate install) | `brew install node` |
| decktape | recommended PDF export; fetched on demand by `npx -y decktape`, bundles its own Chromium | nothing to install |
| gh CLI | create new decks from this template in one command | `brew install gh` |
| Chrome | only for the manual `e`-print fallback | https://google.com/chrome |
| poppler | optional: `pdfinfo` to verify exported page size/count | `brew install poppler` |

On Linux, substitute your package manager; Quarto and Node are the only
hard requirements for the core loop (edit, preview, export).

## The sizing model

RevealJS does not reflow slides. It lays every slide out on a fixed
authored canvas (`width` x `height`) and scales that whole canvas with a
CSS transform to fit the window. Three settings govern everything:

- `width` / `height`: the authored canvas. Pick the aspect ratio of the
  TARGET DISPLAY (1244x700 = 16:9 for projectors; Quarto's default
  1050x700 is 3:2 and will letterbox on widescreen). Changing these
  re-wraps every slide, so set them once, first.
- `margin`: viewport fraction kept empty around the deck. Uniform only;
  there is no per-side margin.
- `max-scale`: scaling clamp, default ~2. On large or high-DPI displays
  the deck stops growing at 2x and sits small in the middle, which looks
  exactly like "fullscreen is broken". Set 9.9 to unclamp.

Letterboxing on one axis when the screen's ratio differs from the
canvas's is geometry, not a bug. Live with it or change the canvas.

## Rules that keep decks healthy

1. **The theming ladder.** Change one documented thing at a time; re-test
   fullscreen (`f`) and print (`e` then Cmd+P) after each change. Custom
   scss may set documented Sass variables freely; treat every structural
   CSS rule (positioning, padding, pseudo-elements on slides) as guilty
   until proven layout-inert. Chrome that adds height to sections causes
   overflow; absolutely-positioned overlays that add no height are the
   only safe kind.
2. **Footers live in the margin zone.** Quarto's `footer:` is viewport
   chrome drawn near the bottom edge. With `margin` below ~0.04,
   bottom-heavy slides can collide with it. Footer + tiny margin: pick one.
3. **Clean-render after theme edits.** `quarto preview` can serve a stale
   compiled theme after scss changes. If a theme edit seems to do nothing:
   `rm -rf .quarto *_files *.html && quarto render`.
4. **Content overflow is editorial, not technical.** If slide content
   crosses the canvas edge, trim the slide or add `{.smaller}` to its
   heading. No margin or scaling value fixes an overfull slide.
5. **Keep the canvas honest while editing** by enabling
   `themes/editing-guide.scss` in the theme list: it draws a dashed
   outline at the true canvas edge (layout-inert). Remove it before
   delivery.
6. **Nothing before the first `##`.** Any content between the YAML block
   and the first slide heading (even an HTML comment) becomes an invisible
   blank slide and shifts every slide index. Put header comments inside
   the first slide.
7. **Never commit render artefacts** (`.quarto/`, `*_files/`, `*.html`):
   the `.gitignore` here already excludes them. Source-HTML assets (such
   as a `background-iframe` animation page under `assets/`) are inputs,
   not render output; they must be tracked, and the `.gitignore` carries
   negation rules covering root `assets/` and the examples. The
   example's `_freeze/` store is also
   committed deliberately: it holds executed figure results so a
   re-render needs no Python, which makes it an input in this rule's
   sense, not a render artefact. Note that `freeze` only applies to
   PROJECT renders: run `quarto render` (no filename) inside the
   example folder. Naming the file (`quarto render keynote.qmd`)
   always re-executes the code and therefore needs Python. The store
   must also stay complete; if any stored file is missing, Quarto
   silently falls back to executing. Keep repos out of synced folders
   (Seafile/iCloud/OneDrive); render output is file-count poison
   for sync engines.

## PDF export

- **Recommended: decktape**, via `./export.sh http://localhost:4200/ deck.pdf`
  (against a running preview server). Slide-faithful pages at the deck's
  exact geometry; scriptable and repeatable; videos become static frames.
- Manual fallback (documented Quarto flow): open the deck in Chrome,
  press `e` (print-pdf mode), Cmd+P, save as PDF, margins none,
  background graphics on.
- Headless `chrome --print-to-pdf` ignores the deck's page geometry and
  produces letter-size pages. Do not use it.

## Themes

Stylesheets live in a `themes/` folder in every project: the starter
and the example share the same shape.

- `themes/plain.scss`: commented scaffold, documented variables only.
- `themes/catppuccin-hku.scss`: Catppuccin Latte, as used for HKU
  COMP1117 decks.
- `themes/editing-guide.scss`: editing aid only; draws a dashed,
  layout-inert outline at the true canvas edge (rule 5).

Swap via the `theme:` list in `deck.qmd`. The two colour themes contain
zero structural rules by design; see rule 1 before adding any.

## Decorative background animation

Ambient background animation (drifting glows, gradients) needs no video
and no JavaScript. Put the animation in a small self-contained HTML page
(CSS `@keyframes` on blurred gradient elements, a few KB) and attach
it to a slide with the documented attribute:

    ## {background-iframe="assets/animation.html"}

RevealJS renders the page as that slide's full-bleed background layer,
behind the content, pointer events off. The deck's markdown stays plain
and the CSS never touches the deck's own layout. Working example:
`examples/keynote/assets/bokeh.html` (an 18-blob field with drift
and pulse loops, de-synced so the ensemble never visibly repeats, plus a
`prefers-reduced-motion` switch).

Practical notes:

- Reserve `background-video` for CONTENT footage. Pre-rendering
  decorative animation to video loses seamless looping, resolution
  independence and reduced-motion support, and adds autoplay risk.
- Screenshot and PDF export freeze the iframe at a frame (verified
  with decktape export and headless-Chrome screenshots).
- `embed-resources` does NOT inline iframes: a single-file delivery
  render must either ship the assets folder alongside, or swap the
  attribute for `background-image="assets/animation-static.png"`.

## The example

`examples/keynote/` shows what a full designed deck looks like when it
is built almost entirely from documented Quarto features, plus two
contained extensions (the routes in `CLAUDE.md`): a dark theme set
through Sass variables, markdown content, columns and cards, fragments for
progressive reveals, an executable matplotlib figure (with `freeze`, so
a project render, `quarto render` with no filename, needs no Python;
see rule 7), pre-rendered background art, and a
CSS-animation background asset. Its theme is a reusable design system
with human-readable classes (title-slide zones, content distribution,
highlight spans, cards) documented by the deck's own class-reference
slides. Start here to see how much a deck can do inside the rules above.

The slides are rebuilt from a selection of a real delivered keynote, so
the content is an excerpt by design: chapter numbers are non-contiguous,
the footer names the original event, and some speaker notes refer to
what happened in the live talk. Treat these as context, not errors; the
example exists to demonstrate the design system, not the talk.

`CLAUDE.md` in the repo root records the working method for AI-assisted
sessions. The sizing model applies to every deck.
