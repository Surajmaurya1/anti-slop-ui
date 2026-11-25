# Component design

Each component has two layers:

- **Behavior and accessibility (mandatory).** Applies in every visual direction.
- **Style (direction-dependent).** Varies with the chosen direction; this file gives defaults and examples of how it can vary.

When *polishing* an existing component, change style only (visual-only policy). Behavior notes here are checks and findings to report, not edits to make without permission.

## Contents
1. Universal checklist for every component
2. Buttons
3. Inputs and form controls
4. Chips, badges, tags
5. Tabs, segmented controls, filters
6. Cards, rows, and when content stays on the page
7. Navigation
8. Overlays
9. Data interfaces
10. Feedback
11. Avoiding "everything is the same rounded rectangle"

---

## 1. Universal checklist

- Clear hierarchy: what is primary, secondary, tertiary.
- All states exist and look intentional: default, hover, focus-visible, active/pressed, disabled, loading, error, selected, empty where relevant.
- Uses tokens only; no stray hex or magic numbers.
- Accessible name, role, and state are exposed (native elements first).
- Keyboard operable with a visible focus indicator.
- Target size meets the floor (>= 24px; 44px on touch-primary).
- Works at narrow widths and with long text.
- Motion (if any) is short, purposeful, and respects reduced motion.

## 2. Buttons

**Behavior [MUST]:** use `<button>` for actions and `<a>` for navigation; disabled buttons use `disabled` (or `aria-disabled` with explanation if focus must remain); loading state keeps width and announces progress; icon-only buttons have an accessible name.

**Hierarchy [DEFAULT]:** one primary action per region (or per screen in focused flows); secondary for alternatives; tertiary/ghost for low-emphasis; destructive for irreversible actions.

**Style [CONTEXT]:**

| Variant | Restrained direction | Expressive direction |
|---|---|---|
| Primary | inverse-neutral or single brand fill | brand fill, gradient, or bold color with offset shadow |
| Secondary | tonal fill or 1px outline | outlined with brand color, or alternate brand hue |
| Tertiary / ghost | text + hover tint | underlined or color-shift text |
| Destructive | ghost/outline with destructive text; solid only at confirmation | solid destructive with confirmation |
| Radius | family radius (not pill) | pill is fine if it is the direction's shape language |
| Feedback | surface-step on hover/press | color, shadow, or transform shifts (keep subtle on press) |

Focus: a 2px ring with offset, >= 3:1 against adjacent colors.

## 3. Inputs and form controls

**Behavior and a11y [MUST]:**
- Every control has a programmatically associated visible label (`<label for>` or wrapping). Placeholder is not a label.
- Helper and error text are linked with `aria-describedby`; invalid fields set `aria-invalid="true"`; required fields are indicated visibly and programmatically.
- Use correct `type`, `inputMode`, and `autocomplete` tokens.
- Do not block paste or password managers.
- The control boundary (border or fill difference) is at least 3:1 against its surroundings (WCAG 1.4.11). Decorative hairlines do not meet this; use `--border-input`.

**Style [CONTEXT]:** height per density mode; radius from the family; fill vs outline vs underline per direction; leading/trailing adornments (icon, kbd hint, unit) inside the same bordered shell; focus ring or border-color change plus ring.

Controls:
- **Text, search, textarea:** label above (most readable); search may use an accessible name and an icon.
- **Checkbox / radio:** visual 16-20px with a 44px hit area on touch; group related controls in `fieldset/legend`.
- **Switch:** only for immediate on/off settings; label states the setting, not the action; expose as `role="switch"` or a checkbox.
- **Select:** native `<select>` unless a custom one gives real value; custom menus must follow combobox/listbox keyboard patterns.
- **Validation messages:** specific and actionable ("Use at least 12 characters"), shown near the field and summarized for long forms. Do not rely on color alone.

## 4. Chips, badges, tags

- **Prompt/filter chips:** outlined or tonal; they are interactive, so they are `<button>` (or links); selected state is `aria-pressed` or checked.
- **Entity chips (inline):** small, tonal, with a glyph and text; non-interactive unless they link.
- **Status badges:** soft tint plus text and/or icon; never color alone.
- **Counts:** muted numerals beside labels; use `tabular-nums`.
- Pill radius is normal here.

## 5. Tabs, segmented controls, filters

Choose by what the control *does*:

| Control does | Use | Notes |
|---|---|---|
| Switches between panels of content | **Tabs** (`role="tablist"`, `tab`, `tabpanel`, arrow-key navigation) | Active tab linked to its panel |
| Filters or sorts one list, mutually exclusive | **Radio group styled as segmented control** | Native radios give arrow-key behavior for free |
| Toggles independent options | **Toggle buttons** (`aria-pressed`) | |
| Navigates to different pages | **Links** in a `<nav>` with `aria-current="page"` | Not tabs |

Style: container pill or square per radius family; active segment raised or filled; counts muted. An executable radio-based example is in `implementation.md`.

## 6. Cards, rows, and when content stays on the page

**Use a card or row when** the item is an *object* the user acts on or navigates into (a product, a message, an app, an approval request) or needs separation to scan (a list of comparable items).

**Keep content directly on the page when** it is prose, a simple section, or a form: wrapping it in a card adds boxes without adding meaning.

Row anatomy (rich list): `[leading tile or avatar] [title + meta line with inline chips] [trailing status/time/action]`. The whole row may be a link/button; keep nested interactive controls accessible (avoid nesting a button inside a link; use a stretched-link pattern if needed).

Nesting: at most two surface levels (page > card > inset). More becomes visual noise.

Card style by direction: tonal fill (neutral), border (calm/enterprise), image-led with soft shadow (commerce), thick border and hard shadow (neo-brutalist), glass over imagery (expressive; keep text on an opaque or sufficiently dimmed layer).

## 7. Navigation

- **Sidebar:** grouped items, active state with fill and `aria-current`, collapsible with a labeled control, search/command entry if the product warrants it.
- **Top nav (marketing):** logo, a few clear links, one primary action; sticky only if useful.
- **Breadcrumbs:** `<nav aria-label="Breadcrumb">` with an ordered list; current page not a link (`aria-current="page"`).
- **Stepper:** show progress and step names; steps that are links must be focusable; announce current step.
- **Mobile:** bottom tab bar (3-5 destinations) for app-like products, or a menu button with a sheet for content sites. Not a desktop sidebar squeezed to icons without labels.
- **Skip link** to main content on pages with substantial chrome.

## 8. Overlays

**Dialog / modal [MUST]:** native `<dialog>` with `showModal()` or a vetted primitive; focus moves in, is trapped, and returns to the trigger on close; Esc closes; labeled by its title; background inert. Title, description, and clear primary/secondary actions with the primary last (or per platform convention).

**Popover / dropdown / menu:** opens on activation (click/Enter/Space), not hover only; arrow-key navigation for menus; closes on Esc and outside click; does not obscure the focused element.

**Tooltip:** supplementary only; appears on focus as well as hover; content is available elsewhere if essential; dismissible (WCAG 1.4.13).

**Sheet (mobile):** bottom sheet with a grab handle; focus management as a dialog.

Style: border-and-shadow combinations per direction; backdrop dimming (blur only when it serves the direction and keeps legibility); enter in 120-220ms with opacity and a small offset.

## 9. Data interfaces

- **Tables:** real `<table>` with `<th scope>`; right-align numerals with tabular figures; sticky header for long tables; row hover; sortable headers are buttons with `aria-sort`. On narrow screens: stacked rows (title plus key meta), horizontal scroll inside a labeled region with a visible affordance, or a column-priority approach. Row height per `tokens.md` section 9.
- **Charts:** one message per chart; direct labels over legends when possible; minimal gridlines; color-blind-safe palettes; highlight the datum the text is about; never rely on color alone (use labels, patterns, or position); provide a text summary or data table alternative.
- **Metrics:** number, label, optional delta; only real metrics; consider whether a metric deserves to be a "KPI card" or just a line in a sentence.
- **Lists with filters:** filter control above, results below, an empty state for no results, and a live-region announcement of result count.
- **Dashboards:** structure follows the user's decisions, not a template. Start from "what does this user need to decide, and what do they look at first?".

## 10. Feedback

- **Toast:** short; `role="status"` (or `alert` for errors); does not disappear while it contains an action the user may need; enough time to read (at least 5 seconds for short messages, longer for more text).
- **Inline alert:** icon + title + message + optional action; severity color is secondary to text and icon.
- **Empty state:** says what lives here and offers the next action; an illustration only if it serves the brand.
- **Error state:** what failed, why if known, how to recover. Keep the user's input.
- **Loading:** skeletons that match the final layout; spinners for short, indeterminate actions; progress bars when you know progress. Respect reduced motion for shimmer.
- **Status transitions** (idle, working, done): change text and icon together; announce to assistive tech.

## 11. Avoiding "everything is the same rounded rectangle"

- Vary component shape language by role: rows are not cards; chips are not buttons; inputs are not cards.
- Use whitespace, rules, and typography for grouping before reaching for another box.
- Let one or two components be signature elements (a distinctive empty state, a unique selected state, a memorable primary button) and keep the rest quiet.
