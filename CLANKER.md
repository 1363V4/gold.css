# AGENTS.md

## CSS: the `g` framework

This project uses a tiny hand-written CSS framework (`<path/to/framework.css>`). Its job is narrow:

1. Short class abbreviations (Tailwind-style) for what I do on every page: centering, stacking, full-height body, reader-width `main`, overlays, and golden-ratio spacing and type sizes.
2. A sane reset.

It has **no opinion about anything visual**: colors, fonts, borders, shadows, blend modes, backgrounds, transitions and so on are the interesting part, and you write them as plain, modern CSS in the project's own stylesheet. Use the framework for the boring 80%, hand-write the rest.

The framework file is the source of truth. Read it before relying on this document, and **do not edit it unless asked**.

### The rules of the system

- **One dial.** `--m` (default `1rem`) drives everything: root font size, spacing, type sizes.
- **One breakpoint.** `@media (width < 567px)` is "mobile". There is no tablet or desktop breakpoint.
- **Center with `gc`.** Almost everything is centered by putting `gc` on the parent.
- **Stack with `gz`.** Cool effects come from layering children in one `gz` parent.
- **`gf`** is the full-height body. **`gw`** is reader mode for `main`. **`go`** is an overlay.
- **Utilities** (`gp-*`, `gm-*`, `gt-*`) all walk down the same scale: `xxs xs s m l xl xxl`.
- **Everything else is custom CSS.**
- Every framework class starts with `g`. Never use that prefix for project classes.

### Which class do I use?

| I want | Use |
|---|---|
| Page fills the viewport (and grows with content) | `gf` on `<body>` (or one root wrapper) |
| Readable centered column for the page content | `gw` on `<main>` |
| Center children on both axes | `gc` on the parent |
| Layer children on top of each other | `gz` on the parent |
| Stack and center | `gc gz` |
| Center vertically, but children full width | `gc gs` |
| Two columns with a golden split | `gg01` / `gg10` (or `gg01d` / `gg10d` to stack on mobile) |
| Modal, menu, toast, lightbox | `go gc` + Datastar `data-show` |
| Padding, margin or font-size from the scale | `gp-*`, `gm-*`, `gt-*` |
| Gap, one-sided spacing, colors, borders, anything else | Custom CSS, using the tokens below |

## Tokens and the dial

The scale is the golden ratio (`--phi`) applied to `--m`:

| Token | Formula | At default dial |
|---|---|---|
| `--xxs` | `m × φ⁻³` | ≈ 0.236rem |
| `--xs` | `m × φ⁻²` | ≈ 0.382rem |
| `--s` | `m × φ⁻¹` | ≈ 0.618rem |
| `--m` | the dial | 1rem |
| `--l` | `m × φ` | ≈ 1.618rem |
| `--xl` | `m × φ²` | ≈ 2.618rem |
| `--xxl` | `m × φ³` | ≈ 4.236rem |

`html` also gets `font-size: var(--m)` and `line-height: 1.618`.

**Use the tokens in custom CSS** instead of hard-coded values: `gap: var(--s)`, `border-radius: var(--xs)`, `padding-inline: var(--l)`, `margin-block-end: calc(var(--m) * 2)`.

**Turning the dial:** set `--m` once on `:root`, in unlayered project CSS, and use an absolute unit:

```css
:root { --m: 18px; }
```

Do not use `rem` or `em` for the dial. `html` font-size is itself `var(--m)`, so a rem value is applied twice (once to the root font size, then again as a multiplier on that root size). Spacing would scale quadratically while text scales linearly.

## Class reference

### Screens

- **`gf`**: `min-width: 100%; min-height: 100dvb`. Full body. Put it on `<body>` or a single root wrapper. It fills the viewport and still grows with content.
- **`gw`**: reader mode. `padding-inline: 19.1dvw` (a centered column of about 61.8% of the viewport); below 567px it becomes `calc(var(--m) / 2)`. Use it on `<main>` only. It is relative to the viewport, so never nest it.
- **`go`**: overlay. `position: absolute; z-index: 1618; inset: 50%; justify-content: center; align-content: center`. It sets no `display`, so **always pair it with `gc`**. Details in "Overlays with Datastar" below.

### Layouts

All three are `display: grid` and style the **direct children** only.

- **`gc`**: children get `place-self: center`. It is a single-column grid, so children stack vertically and each is shrink-wrapped and centered on both axes. If a child must be full width, give it `inline-size: 100%` or add `gs`.
- **`gz`**: children get `grid-area: 1 / 1`, so they all occupy the same cell and paint in DOM order (later is on top). Reach for `z-index` only when DOM order isn't enough.
- **`gs`**: children get `justify-self: stretch`. It comes after `gc` in the stylesheet, so `gc gs` means "centered vertically, stretched horizontally".

Layout classes combine freely (`gc gz`, `gc gs`) because each only sets a few properties on the children.

### Grids

Two children, two columns, one row, golden split. Read the digits left to right, `0` = small column, `1` = large column.

| Class | Columns | Below 567px |
|---|---|---|
| `gg01` | `1fr 1.618fr` | stays two columns |
| `gg10` | `1.618fr 1fr` | stays two columns |
| `gg01d` | `1fr 1.618fr` | one column, rows `1fr 1.618fr` |
| `gg10d` | `1.618fr 1fr` | one column, rows `1.618fr 1fr` |

Use the `d` variants for content that should stack on phones (text beside an image). Use the plain ones when the pair must stay side by side. They expect exactly two children; they don't align the children, so add `gc` to center each cell's content (`gg10d gc`).

### Utilities

Sizes: `xxs xs s m l xl xxl`.

- `gp-{size}`: `padding` on all sides.
- `gm-{size}`: `margin` on all sides.
- `gt-{size}`: `font-size` only (line-height stays `1.618`; tighten it in custom CSS on big headings).

That is the complete list (21 classes). There are **no** directional variants (`gp-x-l`), no `gap` utility, no flex utilities, no color, width or height utilities. For any of those, write CSS with the tokens.

## Overlays with Datastar

`go` plus `gc` plus a Datastar signal:

```html
<body class="gf" data-signals="{menuOpen: false}">
  <button data-on:click="$menuOpen = true">Menu</button>

  <div class="go gc" data-show="$menuOpen" style="display: none">
    <nav class="menu gp-l">
      <!-- content -->
      <button data-on:click="$menuOpen = false">Close</button>
    </nav>
  </div>
</body>
```

- Match the Datastar attribute syntax already used in the project (it varies by version). `style="display: none"` avoids a flash before Datastar runs.
- `go` is a **zero-size box anchored at the center** of its containing block (`inset: 50%`). Its content is centered on that point and overflows equally. Give the child an explicit size (`inline-size: min(90dvw, 40rem)`, `width: max-content`, etc.) instead of relying on intrinsic width, or text may wrap to its narrowest.
- It is `position: absolute`: it anchors to the nearest positioned ancestor, or the initial containing block if there is none. Give the intended parent `position: relative`, or override with `position: fixed` in custom CSS if it must stay in view while scrolling.
- No backdrop, dimming or blur is provided. Write it yourself.
- Don't put the `hidden` attribute on an element controlled by `data-show`. The reset's `[hidden] { display: none !important }` would keep it hidden forever.

## Stacking with `gz`

```html
<section class="gz">
  <img class="cover" src="hero.jpg" alt="">   <!-- custom: inline-size/block-size 100%, object-fit: cover -->
  <div class="tint"></div>                    <!-- custom: gradient, mix-blend-mode, etc. -->
  <div class="gc"><h1 class="gt-xxl">Title</h1></div>
</section>
```

In a plain `gz`, normal children stretch to fill the shared cell, but replaced elements (`img`, `svg`, `video`) don't; size them in custom CSS. `gc gz` on one element centers every layer instead, so nothing stretches.

## What the reset does (don't rely on browser defaults)

- `box-sizing: border-box` everywhere; **all margins and padding are zero**. Paragraphs, lists and headings have no spacing until you add it.
- **Headings inherit font size and weight**, so `<h1>` looks like body text. Style with `gt-*` and custom CSS (`font-weight`).
- Lists lose their padding but keep their markers; set `list-style` / `padding-inline-start` when you want bullets.
- Links inherit color (still underlined). Buttons, inputs, selects and textareas inherit font, color and letter-spacing and have a transparent background; style them yourself.
- `button:enabled` gets `cursor: pointer`. `select` uses `field-sizing: content`.
- `img`, `svg`, `video`, `canvas`, `iframe` and friends are `display: block; max-inline-size: 100%`.
- `hr` is a 1px `currentColor` line at full width. Tables use `border-collapse: collapse`.
- `dialog` and `[popover]` have `margin: auto`. `html` has `text-wrap: pretty`.

## Cascade layers and custom CSS

The framework declares `@layer reset, config, screens, layouts, grids, utilities;`, and all its rules live in those layers.

- **Write project CSS unlayered.** Unlayered styles beat every layer, whatever the specificity. Don't use `!important`, extra specificity or new layers to override the framework.
- The flip side: custom CSS **overrides** utility classes on the same property. If an element has `gp-m` and your CSS also sets `padding`, yours wins. Pick one per property.
- Don't put two utilities from the same family on one element (`gp-m gp-l`). The one defined later in the stylesheet wins.
- Match the framework's style: native CSS nesting, range media queries (`@media (width < 567px)`), logical properties (`padding-inline`, `max-inline-size`), and modern units (`dvb`, `dvw`).

## Do

- Reach for `gc`, `gz`, `gf`, `gw`, `gg*` before writing your own grid or flex layout.
- Use semantic HTML and let the framework classes handle layout and scale.
- Use the tokens for every spacing, gap, radius and font-size decision.
- Write colors, borders, shadows, blend modes, animation and one-off layout in plain CSS.
- Reuse the single breakpoint when a custom rule needs a mobile variant.

## Don't

- **Don't invent classes.** `gp-3`, `gap-m`, `gt-2xl`, `gp-x-l`, `gc-row` and the like don't exist and fail silently. If something is missing, write CSS with the tokens, or ask before extending the framework.
- Don't add Tailwind, normalize/reset sheets, or utility libraries.
- Don't hard-code `px`/`rem` for spacing or type when a token fits.
- Don't introduce additional breakpoints.
- Don't nest `gw`, and don't use it anywhere but `main`.
- Don't set `--m` in `rem`/`em`, and don't set `font-size` on `html`/`:root` directly.
- Don't rely on browser default margins, heading sizes or list styling.

## Minimal page skeleton

```html
<body class="gf">
  <main class="gw gp-l">
    <h1 class="gt-xl">Title</h1>
    <p>Reader-width content.</p>

    <div class="gg10d gc">
      <p>Large column</p>
      <img src="figure.jpg" alt="">
    </div>
  </main>
</body>
```