# Styles catalog

Visual directions to offer, combine, or use as a starting point. These are **illustrations of coherent decision sets, not templates and not rules.** Every direction can be done well or generically. What separates the two is whether each choice has a reason tied to the product and audience.

Values are indicative starting points (inferred from general design practice, not measured from any single source). Tokens for four of them are in `tokens.md`.

## Contents
- How to use this catalog
- 12 directions
- Combining directions
- Building a custom direction
- Direction-independent quality bar

---

## How to use this catalog

1. Match the **product and audience** first, then pick candidates.
2. Offer 3-5 relevant directions in intake, not all twelve, and always allow custom answers.
3. A direction is a set of coordinated decisions: **color, type, shape, surface, density, motion, imagery**. Change one, check the rest still agree.
4. A direction never overrides the brand or existing design system. It fills the gaps.

---

## 1. Precise neutral

**Best for:** developer tools, productivity and workflow apps, admin and settings UIs, anything used for long sessions.
**Look:** quiet and tool-like. Layered gray surfaces, hairline borders, one restrained accent, tight alignment.
**Color:** neutrals 85-95% of pixels; one accent or an inverse (high-contrast) primary; status colors reserved for status; small pastel tiles to identify entities if useful.
**Type:** one clean sans (Inter-like), 13-15px body, even weights, strong contrast between primary and secondary text.
**Shape & surface:** radii 6-12px, 1px borders, shadows rare (borders do the work in dark mode).
**Motion:** fast (120-180ms), state changes only.
**Watch out:** can become anonymous. Give it one ownable trait (a type choice, a distinctive accent, a signature empty state).

## 2. Warm and friendly commerce

**Best for:** e-commerce, food, lifestyle, subscriptions, marketplaces.
**Look:** product-forward and inviting. Warm off-white backgrounds, confident brand color, generous imagery, clear price and action hierarchy.
**Color:** warm neutrals plus one strong brand color; a secondary accent for promotions; tinted chips for categories. Colorful is welcome; roles must be clear (action vs. sale vs. info).
**Type:** friendly humanist or rounded sans, optional serif for headings; legible prices (tabular numerals).
**Shape & surface:** 8-16px radii, soft borders, light shadows on product cards only.
**Motion:** quick feedback on add-to-cart, image hover/zoom, subtle skeleton loading.
**Watch out:** over-decorating with badges and banners; hiding the primary action; fake urgency or fake reviews.

## 3. Playful and bright

**Best for:** consumer apps, education, kids/family, games, community products.
**Look:** personality first. Saturated multi-color palette, chunky shapes, expressive illustration or mascots, rounded type.
**Color:** 3-5 saturated hues with defined roles (primary, secondary, reward, alert); dark ink for text; white or cream surfaces.
**Type:** rounded or geometric display for headings, very legible body; larger sizes than usual.
**Shape & surface:** large radii (16-28px), thick outlines or hard offset shadows optional, big touch targets.
**Motion:** springy, rewarding (confetti or bounce for achievements), always skippable and reduced-motion safe.
**Watch out:** low contrast on bright fills (check every pair), visual noise, motion that blocks input.

## 4. Editorial

**Best for:** publications, portfolios of writing or photography, brand stories, long-form products.
**Look:** paper-and-ink. Strong grid, big confident type, deliberate whitespace, imagery with captions.
**Color:** near-black ink on warm or white paper; a single accent for links and emphasis; color usually comes from imagery.
**Type:** a serif or high-contrast display for headlines paired with a clean text face; careful measure (55-75 characters), real hierarchy.
**Shape & surface:** square or small radii, rules (lines) instead of boxes, little to no shadow.
**Motion:** restrained: reveal on scroll, image transitions.
**Watch out:** poor mobile reflow of big type, low-contrast gray text, decorative drop caps with no purpose.

## 5. Dark developer tool

**Best for:** IDE-like tools, observability, CLI companions, API consoles, terminals.
**Look:** deep dark surfaces, monospace accents, dense information, syntax-color-inspired accents.
**Color:** blue-black layered surfaces; one luminous accent (teal, green, amber, or violet); semantic colors tuned for dark backgrounds.
**Type:** sans for UI, monospace for code, IDs, and numbers; small but legible sizes (12-14px).
**Shape & surface:** 4-8px radii, borders over shadows, subtle surface steps.
**Motion:** nearly none; instant feedback; no animation on data refresh that hinders reading.
**Watch out:** pure-black-and-pure-white harshness, neon overload, tiny low-contrast gray text.

## 6. Expressive gradient / glass

**Best for:** consumer AI, music, media, creative tools, launch moments, brands whose identity *is* color and light.
**Look:** luminous. Gradients, blur, glow, depth, often over rich backgrounds.
**Color:** a deliberate gradient palette drawn from the brand (not a default purple-blue); solid, legible surfaces under text.
**Type:** confident sans or display; generous size for headlines; keep body text on opaque or sufficiently dimmed surfaces.
**Shape & surface:** frosted layers with enough opacity for contrast, soft glows, large radii.
**Motion:** slow ambient shifts, parallax used sparingly; honor reduced motion; keep GPU cost in mind.
**Watch out:** the generic version (random purple-blue mesh, glass cards everywhere, floating orbs with no meaning); contrast of text over blur; performance on low-end devices.

## 7. Neo-brutalist

**Best for:** indie products, creative studios, bold consumer brands, anything that wants to feel raw and human.
**Look:** flat saturated color blocks, thick black borders, hard offset shadows, raw or monospace type, intentional "unfinished" feel.
**Color:** limited bold palette (e.g. yellow, pink, blue) on off-white or cream; black ink.
**Type:** heavy grotesque or mono; large, tight.
**Shape & surface:** 0-8px radii, 2-3px borders, hard shadows (no blur).
**Motion:** snappy offset shifts on hover/press.
**Watch out:** accessibility of colored text on colored blocks; consistency of border/shadow rules; fatigue in dense apps.

## 8. Soft and calm

**Best for:** health, wellness, personal finance, family tools, anything that needs trust and reassurance.
**Look:** gentle and clear. Soft surfaces, calm hues, rounded forms, reassuring copy.
**Color:** muted blues/greens/sands with one friendly accent; careful, clear status colors.
**Type:** warm sans, comfortable size (16px+ body), generous line height.
**Shape & surface:** 12-20px radii, soft shadows or tonal surfaces, large tap targets.
**Motion:** slow, soothing, minimal.
**Watch out:** washed-out contrast, vague hierarchy, playful tone where seriousness is needed (money, medical).

## 9. Luxury / premium

**Best for:** high-end retail, hospitality, architecture, jewelry, fashion, premium services.
**Look:** restrained and refined. Generous space, large imagery, delicate type, rare accent.
**Color:** deep neutrals or ivory with a single metallic or jewel accent used sparingly.
**Type:** elegant serif or wide-tracked sans for display; thin weights only at large sizes (never for body text); refined small caps or letterspacing for labels.
**Shape & surface:** square or very small radii; fine rules; almost no shadows.
**Motion:** slow, smooth, cinematic reveals; never janky.
**Watch out:** thin low-contrast text, heavy image weight, mobile usability lost to "airiness".

## 10. Maximalist / creative portfolio

**Best for:** designers, studios, artists, experimental brands, campaign sites.
**Look:** oversized type, asymmetry, collage, layered imagery, rich motion and interaction.
**Color:** whatever expresses the work; high-contrast pairings; color as structure.
**Type:** expressive display faces, mixed scales, variable-font play; a quiet text face for reading.
**Shape & surface:** unconstrained, but internally consistent rules.
**Motion:** rich: scroll-linked, cursor-aware, page transitions. Provide a calm fallback (reduced motion) and keep content reachable.
**Watch out:** content and navigation getting lost, performance, motion sickness, unreadable text over busy imagery. Maximalism needs *more* system, not less.

## 11. Enterprise calm

**Best for:** B2B software, finance operations, analytics, HR, internal tools with dense data.
**Look:** clear, dense, trustworthy. Tables and forms done very well; conservative color.
**Color:** blue-gray neutrals, one brand color, strictly semantic status colors, colorblind-safe chart palettes.
**Type:** system or neutral sans, 13-14px, tabular numerals, clear table headers.
**Shape & surface:** 4-8px radii, thin borders, subtle zebra or row hover, modest shadows on overlays only.
**Motion:** minimal and functional.
**Watch out:** the generic KPI-cards-plus-line-chart dashboard for every product; undifferentiated screens; insufficient empty and error states.

## 12. Retro / nostalgic

**Best for:** games, community sites, creative projects, brands with a deliberate throwback identity.
**Look:** pixel, Y2K, terminal, print, or analog textures with consistent rules.
**Color:** palette tied to the era referenced; limited and committed.
**Type:** bitmap, mono, or period display faces with a readable fallback for body text.
**Shape & surface:** era-appropriate (hard pixels, bevels, halftones), applied consistently.
**Motion:** period-appropriate (stepped animation), skippable.
**Watch out:** pastiche without purpose; legibility of novelty fonts; accessibility of low-resolution aesthetics.

---

## Combining directions

Combining is encouraged. State which attributes come from which direction and check coherence.

| Combination | Example result |
|---|---|
| Editorial + playful color | Serif headlines and a strict grid, with bright accent blocks and illustrated spots |
| Dark developer tool + expressive gradient | Dark dense UI with one signature gradient reserved for brand moments (logo, hero, empty state) |
| Warm commerce + neo-brutalist | Cream background, thick outlines and hard shadows on product cards, chunky friendly type |
| Soft and calm + precise neutral | Calm hues and large touch targets inside a tight, tool-like layout (a clinical or finance dashboard with a reassuring tone) |
| Enterprise calm + brand-forward color | Dense, clear layouts with a strong, ownable brand accent and illustrated empty states |

## Building a custom direction

When the user describes their own style, translate it into seven decisions and confirm them in the brief:

1. **Personality words** (3-5: e.g. "confident, warm, a little irreverent").
2. **Color:** brand, accent(s), neutrals (tinted or pure), status; role for each; gradient policy.
3. **Typography:** families, pairing logic, weight and size character, numerals.
4. **Shape:** radius family, border weight, outline vs fill.
5. **Surface and depth:** flat, layered, shadowed, glass; what elevation means.
6. **Density and layout:** grid, spacing rhythm, content width.
7. **Motion:** character (instant, smooth, springy, theatrical) and purpose.

## Direction-independent quality bar

Whatever the direction:
- Hierarchy is clear: the primary action and the most important content are obvious.
- Consistency: one radius family, one spacing scale, one type scale, one icon style.
- States are real: hover, focus-visible, active, disabled, loading, empty, error.
- Accessibility floors hold (`accessibility.md`).
- Placeholders are marked; nothing fake is presented as real.
- The interface has a point of view that fits its product, not a default.
