# Instructions for AI sessions working in this repo

Distilled from the sessions that built it. Read README.md first: its rules
are constraints, not suggestions. This file adds the working method.

## The three routes (know which one you are on)

1. **Plain**: documented YAML options, documented Sass variables,
   markdown content, typography-only and simple-box classes. Default.
2. **Middle**: two marked extensions, each with a containment argument:
   - decorative CSS animation encapsulated in a self-contained HTML
     asset, attached via the documented `background-iframe` attribute
     (see `examples/keynote/assets/bokeh.html`);
   - the layout family in `examples/keynote/themes/keynote-theme.scss`
     (`.title-layout` zones, `.spread`, `.fill-space`): flex that sizes
     only its own children.
   Every structural rule added to a theme MUST carry a comment stating
   why it cannot affect other slides, scaling, or print.
3. **Advanced**: raw HTML slides with a bespoke design system. No
   advanced-route example ships in this repo. Whole-deck opt-in; budget
   it as front-end work: you own every pixel, and the sizing model from
   the README still applies unchanged.

## Layout principles (hard-won)

- **Distribution, not spacing.** Never position content with fixed pixel
  spacers; they break when content changes. Use the layout family: zones
  for title slides, `.spread` to distribute content-slide blocks,
  `.fill-space` on the block that absorbs elastic height.
- `.layout-top` and `.layout-bottom` carry no CSS rules by design: flex
  order inside `.title-layout` places them. Do not add rules to them.
- The canvas never reflows, so flex container heights can be fixed
  constants derived from the authored canvas. Document the arithmetic
  next to the constant.
- **Never override Quarto's `.columns`/`.column` display** — it breaks
  their layout engine. To stretch children (tall cards), pass definite
  heights down: `.fill-space { flex: 1 }`, `.column { height: 100% }`,
  card `height: calc(100% - margin)`.
- Class names are human-readable and self-describing
  (`.section-label`, `.highlight-cyan`, `.author-name`). No jargon, no
  abbreviations. Keep the deck's class-reference slides in sync: every
  class rendered next to its name is the theme's living documentation.

## Verification method (what actually worked)

- Per-slide screenshots: headless Chrome,
  `--window-size=1280,720 --virtual-time-budget=6000 --screenshot=out.png "URL#/n"`.
  Caveats: it does NOT drive fragment states from the URL, and a bad
  capture looks like a broken slide — confirm against a decktape export
  (which renders true end states) before "fixing" anything.
- Build a labelled contact sheet (PIL) to check slide alignment and
  overall state cheaply BEFORE dispatching detailed comparisons; phantom
  or shifted slide indices otherwise poison every downstream diff.
- For fidelity work against a target: vision agents compare slide PAIRS
  and return ranked, mechanism-specific differences; fix in consolidated
  rounds; re-shoot only what changed; expect 3-4 rounds.
- After ANY scss edit: `rm -rf .quarto *_files *.html && quarto render`
  — preview's incremental render silently serves a stale compiled theme.
- Preview serving: `quarto preview deck.qmd --port N --host 0.0.0.0
  --no-browser`; a project subfolder serves its deck at
  `/<name>.html`, not `/`.

## Content and judgement rules

- Slide text is the presenter's voice: flatten AI-writing tells
  (paired negation-affirmation closers, manufactured metaphor labels,
  triadic slogans) and avoid em-dashes in prose.
- `background-video` is for CONTENT footage only. Decorative motion
  belongs to CSS (seamless, resolution-independent, honours
  reduced-motion, a few KB); pre-rendering decoration to video is worse
  on every axis and muddies what the plain route can honestly claim.
- Nothing before the first `##` (invisible blank slide). Footers live in
  the margin zone. The full list: README "Rules that keep decks healthy".
- When a request conflicts with fidelity to an existing artefact
  (e.g. voice rules vs faithful excerpting), surface the conflict and
  let the author choose; do not silently pick.
