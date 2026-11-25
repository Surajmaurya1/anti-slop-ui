# Design tokens

A token library to start from, **not a mandate**. Use it to build or map a system for the project in front of you.

## Contents
1. How to use tokens (precedence)
2. Token roles (what to define)
3. Color architecture
4. Presets A-D (CSS)
5. Building a palette for a brand
6. Typography
7. Spacing, radius, shadow, motion
8. Density modes and target sizes
9. Row and control heights
10. Resolved conflicts (formerly contradictory rules)
11. Verification and provenance of the values

---

## 1. How to use tokens (precedence)

1. **Existing tokens win.** If the project already has a coherent token system (CSS variables, Tailwind theme, design-system package), map to it. Do not add a parallel set or rename theirs. If it is incoherent, report that and propose consolidation; do not silently replace it.
2. **Brand and user choices next.** Brand colors, fonts, and the approved brief override preset values.
3. **Presets last.** Use a preset only to fill gaps or when there is nothing yet. Adjust freely for the chosen direction.
4. **One source of truth.** Define each value once (variables or theme), reference it everywhere. No hard-coded hex values in components.
5. Values below are labeled **verified** (checked with `scripts/contrast.py`; the pairs are in `tests/contrast-pairs.txt`) or **inferred** (a reasonable starting point; unmeasured).

## 2. Token roles (what to define)

| Group | Roles |
|---|---|
| Color, structural | `background`, `surface`, `surface-raised`, `surface-muted`, `foreground`, `foreground-muted`, `foreground-subtle`, `border` (decorative), `border-input` (control boundary), `ring` (focus) |
| Color, action | `primary`, `primary-foreground`, `secondary`, `secondary-foreground`, `accent` (optional) |
| Color, feedback | `success`, `warning`, `destructive`, `info`, each with a soft background variant |
| Color, identity (optional) | entity/category hues used for avatars, tiles, tags, chart series |
| Type | families, weights, sizes, line heights, letter spacing |
| Space | a scale (4px or 8px base) |
| Shape | radius scale; border widths |
| Depth | shadow scale (may be empty for flat directions) |
| Motion | durations, easings |

Names are suggestions; match the project's naming if it has one.

## 3. Color architecture

Color has **layers**, each with its own rules. This replaces any "one accent only" or "no color" rule.

| Layer | What it is | How many hues | Rule |
|---|---|---|---|
| Neutrals | background, surfaces, text, borders | 1 ramp (pure or tinted toward the brand hue) | Build depth with surface steps; tint is allowed and often better than pure gray |
| Brand / accent | action, links, selection, emphasis | **Direction-dependent:** 1 for restrained directions; 2-5 for expressive ones | Every hue has a stated role in the brief |
| Feedback | success, warning, error, info | 3-4, reserved for status | Do not repurpose for decoration; always pair with text or icon |
| Identity (optional) | category/entity colors, chart series | a small set, stable assignment | Same entity, same color, always; check contrast of glyph on tile |

Rules that hold in every direction:
- Contrast floors in `accessibility.md` apply to every text, control boundary, and focus pair. [MUST]
- Color is never the only carrier of meaning. [MUST]
- Gradients: allowed when intentional. Define where they live (brand moments, hero, accents) and ensure text sits on a verified-contrast area. [CONTEXT]
- Neutral-first is a **default for restrained directions**, not for all directions. A playful or expressive product may be 40% color. [CONTEXT]

## 4. Presets

All executable CSS (valid custom properties; verified to parse with lightningcss via Tailwind v4's CLI). Rename to match the project.

### Preset A: Precise neutral (light and dark)

Source: generalized from the v0.1.0 reference analysis of seven screenshots of one product. Colors **estimated by eye**, then **corrected for contrast and verified**. Suits tool-like, dense, quiet products. Not a universal default.

```css
:root {
  --background: #fafafa;  --surface: #ffffff;  --surface-raised: #ffffff;  --surface-muted: #f4f4f5;
  --foreground: #0a0a0a;  --foreground-muted: #5f5f68;  --foreground-subtle: #6b6b74;
  --border: #e7e7ea;              /* decorative hairline only */
  --border-input: #8a8a93;        /* control boundary, >= 3:1 on background and surface */
  --ring: #0a0a0a;                /* use 2px with 2px offset */
  --primary: #0a0a0a;  --primary-foreground: #fafafa;
  --secondary: #f4f4f5; --secondary-foreground: #0a0a0a;
  --success: #15803d;  --warning: #b45309;  --destructive: #b91c1c;   /* text-safe on white and on --surface-muted */
  --success-soft: rgba(21,128,61,.12); --warning-soft: rgba(180,83,9,.12); --destructive-soft: rgba(185,28,28,.10);
}
.dark {
  --background: #0a0a0a;  --surface: #161616;  --surface-raised: #1f1f1f;  --surface-muted: #262626;
  --foreground: #f5f5f5;  --foreground-muted: #a0a0a8;  --foreground-subtle: #8e8e97;
  --border: #262626;
  --border-input: #6e6e78;
  --ring: #f5f5f5;
  --primary: #f5f5f5;  --primary-foreground: #0a0a0a;
  --secondary: #1f1f1f; --secondary-foreground: #f5f5f5;
  --success: #4ade80;  --warning: #fbbf24;  --destructive: #f87171;
  --success-soft: rgba(74,222,128,.14); --warning-soft: rgba(251,191,36,.14); --destructive-soft: rgba(248,113,113,.14);
}
```

Verified pairs include: foreground on every surface; muted and subtle text on surface and surface-muted (>= 4.5:1); border-input on its surfaces (>= 3:1); ring on background (>= 3:1); status colors on white and on surface-muted. See `tests/contrast-pairs.txt`.

Note what changed from v0.1.0: subtle text was 2.56:1 on white; input borders were about 1.4:1; focus rings were 1.5:1 and 1.95:1; success and warning text failed 4.5:1. All corrected above.

Optional **identity tiles** (inferred; for 20-28px glyph tiles, dark glyph on pastel): yellow `#fde047`, sky `#93d5fb`, pink `#f0abfc`, peach `#fdba9a`, mint `#a7f3d0`. A dark glyph on yellow measured 15:1; check any other pair you add.

### Preset B: Warm commerce (light)

Inferred starting point; pairs verified.

```css
:root {
  --background: #fffaf5;  --surface: #ffffff;  --surface-muted: #f6efe8;
  --foreground: #1f1a17;  --foreground-muted: #6a5d54;
  --border: #eadfd5;                 /* decorative */
  --border-input: #8c7d72;           /* >= 3:1 */
  --primary: #c2410c;  --primary-foreground: #ffffff;       /* brand action; also safe as link text on background/surface */
  --accent: #0f766e;   --accent-foreground: #ffffff;        /* secondary brand / promos */
  --tint: #fde8d9;     --tint-foreground: #9a3412;          /* soft chips and badges */
  --ring: #c2410c;                                          /* >= 3:1 on background */
  --success: #15803d;  --destructive: #b91c1c;              /* sale and errors */
}
```

### Preset C: Playful bright (light)

Inferred starting point; pairs verified (dark ink on every bright fill; no white text on bright fills).

```css
:root {
  --background: #fffaf0;  --surface: #ffffff;  --surface-muted: #fff1d6;
  --foreground: #14213d;  --foreground-muted: #4b5775;
  --border: #14213d;      --ring: #14213d;       /* ink outlines double as the boundary and focus color */
  --primary: #ff6b35;     --primary-foreground: #14213d;     /* ink on orange */
  --mint: #2ec4b6;  --sun: #ffd23f;  --bubblegum: #ff8fab;   /* all take --foreground text */
  --success: #15803d;  --destructive: #b91c1c;
  --radius-lg: 20px;  --shadow-hard: 4px 4px 0 var(--foreground);   /* optional chunky offset shadow */
}
```

### Preset D: Dark developer tool

Inferred starting point; pairs verified.

```css
:root {
  --background: #0b0d10;  --surface: #12151a;  --surface-raised: #181c22;  --surface-muted: #20252d;
  --foreground: #e6e9ee;  --foreground-muted: #98a1b0;  --foreground-subtle: #8a93a3;
  --border: #232830;      --border-input: #667080;            /* >= 3:1 on surface and raised */
  --accent: #5eead4;      --accent-foreground: #0b0d10;       /* button fill; also fine as text on surfaces */
  --ring: #5eead4;
  --success: #4ade80;  --warning: #fbbf24;  --destructive: #f87171;
  --font-mono: ui-monospace, "JetBrains Mono", "SF Mono", Menlo, monospace;
}
```

## 5. Building a palette for a brand

1. **Start from what exists:** logo, brand guide, existing CSS. Sample actual brand values; do not eyeball when files exist.
2. **Assign roles:** which hue is action, which is emphasis, which (if any) is identity.
3. **Neutrals:** pure or tinted toward the brand hue (hue-matched grays feel cohesive). Build 4-5 surface steps for dark themes, 3-4 for light.
4. **Test pairs:** every text/background, control-boundary/background, and focus/background pair with `scripts/contrast.py`. Adjust lightness (not hue) until it passes; often a brand color works as a fill but needs a darker or lighter sibling for text.
5. **Feedback colors:** pick tones that read as green/amber/red *and* pass contrast; tune per theme.
6. **Dark theme** is not an inversion: use layered off-blacks and off-whites, desaturate and lighten accents, and re-verify every pair.

## 6. Typography

Typography is a direction decision. The values below are defaults for restrained product UI.

| Role | Size / line height | Weight | Letter spacing |
|---|---|---|---|
| Display / hero (marketing, expressive) | clamp(2.25rem, 5vw, 4.5rem) / 1.05-1.15 | 600-800 or per typeface | -0.02em to -0.04em |
| Page title | 1.25-1.5rem / 1.25 | 500-600 | -0.01em |
| Section title | 1-1.125rem / 1.3 | 500-600 | 0 |
| Body | 0.875-1rem / 1.5 | 400 | 0 |
| Secondary / meta | 0.8125-0.875rem / 1.4 | 400 | 0 |
| Caption / label | 0.75rem / 1.35 | 400-500 | 0 to 0.02em |
| Mono | 0.75-0.875rem / 1.5 | 400 | 0 |

- Weights are a **per-direction choice**. Restrained directions may use two (400/500); expressive ones may use the full range or a variable font. **Mandatory:** a consistent role-to-weight mapping, and no thin weights (<300) for body text.
- Body text on mobile inputs is at least 16px to avoid iOS zoom-on-focus.
- Use tabular numerals (`font-variant-numeric: tabular-nums`) for aligned figures.
- Expressive and oversized type is welcome when it serves the direction; ensure reflow at narrow widths and text-spacing overrides.
- Sizes use `rem` so user font settings are respected.

## 7. Spacing, radius, shadow, motion

**Spacing (inferred; 4px base):** `2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 56, 80`. Pick a base (4 or 8) and stay on it. Reduce or increase rhythm per density, not per component.

**Radius (inferred):** choose one **family** per direction and use it consistently.

| Family | xs | sm | md | lg | xl | full |
|---|---|---|---|---|---|---|
| Tight | 2 | 4 | 6 | 8 | 12 | 9999 |
| Standard | 4 | 6 | 8 | 12 | 16 | 9999 |
| Soft | 6 | 10 | 14 | 20 | 28 | 9999 |
| Square | 0 | 0 | 0 | 2 | 4 | 9999 (only for avatars/dots) |

Pill radius is for chips, segmented controls, avatars, and status dots by default; it is allowed for buttons when the direction calls for it (playful, soft).

**Shadow:** direction-dependent. Flat/neutral directions: none or `0 1px 2px rgba(0,0,0,.06)` on raised light surfaces; use borders for dark themes. Soft directions: layered soft shadows. Neo-brutalist: hard offset shadows with no blur. Glass/expressive: glows and blurs, each tied to elevation or focus. Define each as a token; avoid ad-hoc shadows.

**Motion (inferred):** fast 100-150ms (hover, press), normal 160-220ms (menus, toggles), slow 250-400ms (panels, page-level). Easing: `cubic-bezier(.2,.8,.2,1)` for enters; `cubic-bezier(.4,0,.2,1)` for position changes; springs where the direction calls for physical feel. All non-essential motion respects `prefers-reduced-motion`.

## 8. Density modes and target sizes

Define two modes and switch with the input type, instead of one set of sizes.

| Control | Compact (pointer-primary) | Comfortable (touch-primary) |
|---|---|---|
| Button height | 28-36px | 44px |
| Input height | 32-36px | 44-48px |
| Icon button hit area | 28-32px | 44px |
| Menu / list item | 32-36px | 44px |
| Checkbox / radio visual | 16px | 20px (hit area 44px) |

- **[MUST]** every interactive target is at least **24 x 24 CSS px**, or has the spacing exception from WCAG 2.2 SC 2.5.8.
- **[DEFAULT]** touch-primary controls are **44 x 44 px**. A control may look smaller than its hit area (padding or a pseudo-element extends it).
- Switch with `@media (pointer: coarse)` and/or a width breakpoint; do not rely on width alone.

```css
:root { --control-h: 2.25rem; --hit: 2rem; }
@media (pointer: coarse) { :root { --control-h: 2.75rem; --hit: 2.75rem; } }
```

## 9. Row and control heights

| Element | Compact | Comfortable | Notes |
|---|---|---|---|
| Rich list row (icon + title + meta line) | 56px | 64px | two lines of content |
| Simple list row (one line) | 40px | 48px | |
| Table row | 36px | 44-56px | data-dense products may go to 32px; keep hit areas for row actions >= 24px |
| Menu / select option | 32px | 44px | |
| Sidebar nav item | 32px | 44px | |
| Input / button | see section 8 | see section 8 | |

"General row height" and "table row height" are different things; use the matching row, not a global value.

## 10. Resolved conflicts (formerly contradictory rules)

v0.1.0 contained rules that contradicted each other or overreached. They are resolved as follows.

| Former conflict | Resolution |
|---|---|
| "One accent only" vs "entity and status colors" | Color is layered (section 3): neutrals, brand/accent, feedback, identity. Restrained directions use one accent; expressive ones use several. Every hue needs a stated role. |
| "Weights 400 and 500 only" vs expressive type | Weight is a direction choice. Only mandatory: consistent role-to-weight mapping, no thin body text. |
| Desktop button sizes vs mobile touch targets | Two density modes (section 8). 24px is the accessibility floor; 44px is the touch default. |
| Single row height vs table row height | Separate rows in section 9. |
| Neutral defaults vs brand colors | Neutral presets apply only when no brand/direction exists. Brand and approved brief override (precedence in section 1). |
| "No gradients, shadows rare, primary always inverse, pills never on buttons" | These describe Preset A only. Other directions set their own policy; each must be consistent and justified. |
| "Emoji never as icons" | Default is a real icon set. Emoji are acceptable as an intentional brand choice with accessible labels. |

## 11. Verification and provenance of the values

- **Verified:** contrast of every pair in `tests/contrast-pairs.txt` (run `python3 tests/test_contrast.py`).
- **Inferred:** all hex values were chosen or adjusted by the author, not sampled from a screenshot with a measuring tool. The original reference colors in v0.1.0 were estimated by eye from phone screenshots.
- **Not verified:** how these presets look in a real product, in real lighting, or to color-vision-deficient users beyond contrast math.
- See `provenance.md` for the origin and limits of Preset A.
