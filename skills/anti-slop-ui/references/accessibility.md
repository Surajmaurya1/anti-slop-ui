# Accessibility

**Target: WCAG 2.2 Level AA** unless the project or user specifies another standard (e.g. EN 301 549, Section 508, an AAA goal). Accessibility floors are **[MUST]** and are not traded away for aesthetics.

**Do not claim compliance without verification.** "WCAG 2.2 AA compliant" is a conformance claim that requires evaluating the real, rendered interface (including assistive-technology testing). What this skill can honestly say is: "I checked X by method Y; I did not check Z." See section 11.

## Contents
1. Scope: what a visual-only task can and cannot fix
2. Contrast and use of color
3. Keyboard and focus
4. Semantics and screen readers
5. Forms and validation
6. Target size and touch
7. Motion and animation
8. Zoom, reflow, and text spacing
9. Internationalization and RTL
10. WCAG 2.2 criteria that most often matter for visual work
11. How to verify, and how to report

---

## 1. Scope: visual-only vs behavioral accessibility

Because the default scope is visual-only (`SKILL.md` section 5):

| Fix | Treatment |
|---|---|
| Color contrast, focus ring styles, target sizes, spacing, text size, reduced-motion CSS, visible labels via CSS layout, non-color indicators implemented with CSS/icons | **Allowed** (visual) |
| Additive attributes: `aria-label`, `alt`, `lang`, `role` on static elements | **Disclose** in the report; ask first if many |
| Swapping `div`/`span` for `button`/`a`/`label` while preserving all handlers and attributes | **Disclose** |
| Focus trapping, keyboard handlers, live-region logic, form validation messaging logic, new ARIA state wired to behavior | **Behavioral: report as a finding; ask permission before implementing** |

When you find a behavioral accessibility defect during a visual task, record it as a finding (Accessibility track) with evidence and a recommended fix. Do not silently implement it.

## 2. Contrast and use of color

- **Text:** >= 4.5:1; large text (>= 24px, or >= 18.66px bold) >= 3:1 (SC 1.4.3).
- **UI components and meaningful graphics:** >= 3:1 against adjacent colors (SC 1.4.11): control boundaries (inputs, unselected checkboxes), focus indicators, icons that carry meaning, chart marks.
- Decorative hairlines are exempt; the *boundary that identifies a control* is not. Provide a `border-input` token that meets 3:1 (see `tokens.md`).
- Measure every pair, including states (hover, disabled is exempt but should remain discernible), text over images or gradients (test the worst region), and text on tinted/translucent surfaces (composite first). `scripts/contrast.py` handles hex and `rgba()` over a background.
- Never use color alone to convey information (SC 1.4.1): add text, icon, pattern, or position.
- Provide both light and dark verifications if both themes ship.
- Respect `prefers-contrast: more` where practical.

## 3. Keyboard and focus

- Everything operable by mouse or touch is operable by keyboard (SC 2.1.1); no keyboard traps (2.1.2); logical focus order (2.4.3).
- **Focus visible (2.4.7):** never remove outlines without a replacement. Use `:focus-visible`. Recommended appearance: 2px solid ring with 2px offset, >= 3:1 contrast against adjacent colors (this also meets the spirit of 2.4.13, which is AAA).
- **Focus not obscured (2.4.11, new in 2.2):** sticky headers, cookie banners, and chat widgets must not fully cover the focused element. Use `scroll-padding-top` equal to sticky header height.
- Provide a **skip link** when there is substantial repeated chrome.
- Roving tabindex or arrow keys for composite widgets (tabs, menus, radio groups) per the ARIA Authoring Practices; prefer native elements that provide this.
- Custom components must handle Enter/Space for buttons, Esc for overlays.

## 4. Semantics and screen readers

- Native elements first: `button`, `a`, `input`, `select`, `label`, `fieldset`, `nav`, `main`, `header`, `footer`, `ul/ol`, `table`, `dialog`.
- One `<h1>`; heading levels reflect structure, not size. Use CSS for size.
- Landmarks: `main`, `nav` (labeled if multiple), `header`, `footer`, `aside`.
- Accessible names for icon-only controls, images with meaning (`alt`), and decorative images (`alt=""` or `aria-hidden`).
- State is exposed (`aria-expanded`, `aria-pressed`, `aria-selected`, `aria-current`, `aria-invalid`); the visual state always matches the programmatic state.
- Announce dynamic changes with live regions (`role="status"` / `aria-live="polite"`; `role="alert"` for urgent errors) (SC 4.1.3).
- Dialogs: `role="dialog"` with `aria-modal` and a label, or native `<dialog>`; focus is managed (see `components.md`).
- Do not use ARIA to override native semantics unless necessary; no ARIA is better than bad ARIA.

## 5. Forms and validation

- Visible label for every field (SC 3.3.2, 1.3.1); placeholder is a hint, not a label.
- Group related fields with `fieldset`/`legend`.
- Identify errors in text (3.3.1), near the field, and link with `aria-describedby`; offer a correction suggestion where possible (3.3.3).
- On submit with errors: move focus to the first invalid field or an error summary with links.
- `autocomplete` tokens for personal data (1.3.5).
- **Redundant entry (3.3.7, new in 2.2):** do not make users re-enter information already provided in the same flow, unless essential.
- **Accessible authentication (3.3.8, new in 2.2):** do not require a cognitive function test (memorizing, transcribing) to log in; allow paste and password managers.
- Required fields marked in text ("required" or an asterisk explained), not color alone.
- Do not auto-submit on input; do not time out without warning.

## 6. Target size and touch

- **[MUST]** >= 24 x 24 CSS px for pointer targets, or satisfy the spacing exception (SC 2.5.8, new in 2.2).
- **[DEFAULT]** >= 44 x 44 px on touch-primary interfaces (platform and AAA guidance).
- Space adjacent targets so mis-taps are unlikely; extend hit areas with padding or pseudo-elements rather than enlarging visuals.
- Provide non-drag alternatives for drag interactions (2.5.7, new in 2.2).
- Do not rely on hover for essential content; hover/focus-triggered content must be dismissible, hoverable, and persistent (1.4.13).

## 7. Motion and animation

- Wrap non-essential motion in `@media (prefers-reduced-motion: no-preference)`, or provide a `reduce` override that removes parallax, large translations, auto-play, and shimmer; keep essential state feedback (opacity or color changes are generally fine).
- No flashing more than three times per second (2.3.1).
- Anything that moves, blinks, or scrolls automatically for more than 5 seconds needs pause/stop/hide (2.2.2). No auto-playing carousels without controls.
- Avoid scroll-jacking and large parallax that can trigger vestibular symptoms.
- Animation must never delay input or hide content from keyboard users.

```css
/* Executable pattern */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
```

(Use this blunt reset only if the project has no better mechanism; prefer opting animations in under `no-preference`.)

## 8. Zoom, reflow, and text spacing

- Content works at 200% text size (1.4.4) and reflows at 320 CSS px width / 400% zoom without two-dimensional scrolling, except for content that needs it (data tables, maps, diagrams) (1.4.10).
- Use `rem`/`em`, flexible containers, `min-width: 0`, `overflow-wrap: anywhere` where long strings occur; avoid fixed heights on text containers.
- Survives text-spacing overrides (line height 1.5, paragraph spacing 2x, letter spacing 0.12em, word spacing 0.16em) without clipping or overlap (1.4.12).
- Do not disable pinch-zoom (`user-scalable=no` / `maximum-scale=1` are failures).
- Orientation is not locked (1.3.4).

## 9. Internationalization and RTL

- Set `lang` on the document and on language changes.
- Use **logical properties**: `margin-inline-start`, `padding-inline`, `inset-inline-end`, `text-align: start`, `border-start-start-radius`; in Tailwind use `ms-*`, `me-*`, `ps-*`, `pe-*`, `text-start`, `start-*`, `end-*`.
- Set `dir="rtl"` for RTL languages (Arabic, Hebrew, Persian, Urdu) and test the layout by flipping `dir`.
- **Mirror** directional icons and layouts (chevrons, back arrows, progress, sliders); do **not** mirror logos, media controls conventions, clocks, or numerals.
- Allow text expansion (30-40% for some languages) and varying line heights for scripts with tall glyphs (Devanagari, Thai, Arabic).
- Use `<bdi>` or `dir="auto"` for user-generated mixed-direction text.
- Pick font stacks that cover the needed scripts; do not rely on a Latin-only brand font for body text in other scripts.

## 10. WCAG 2.2 criteria that most often matter for visual work

| SC | Level | Topic |
|---|---|---|
| 1.3.4 | AA | Orientation |
| 1.3.5 | AA | Identify input purpose |
| 1.4.1 | A | Use of color |
| 1.4.3 | AA | Contrast (text) |
| 1.4.4 | AA | Resize text |
| 1.4.10 | AA | Reflow |
| 1.4.11 | AA | Non-text contrast |
| 1.4.12 | AA | Text spacing |
| 1.4.13 | AA | Content on hover or focus |
| 2.1.1 / 2.1.2 | A | Keyboard / no trap |
| 2.2.2 | A | Pause, stop, hide |
| 2.3.1 | A | Three flashes |
| 2.4.3 | A | Focus order |
| 2.4.7 | AA | Focus visible |
| **2.4.11** | AA (new in 2.2) | Focus not obscured (minimum) |
| **2.5.7** | AA (new in 2.2) | Dragging movements |
| **2.5.8** | AA (new in 2.2) | Target size (minimum) 24px |
| **3.2.6** | A (new in 2.2) | Consistent help |
| 3.3.1 / 3.3.2 / 3.3.3 | A / A / AA | Error identification, labels, error suggestion |
| **3.3.7** | A (new in 2.2) | Redundant entry |
| **3.3.8** | AA (new in 2.2) | Accessible authentication (minimum) |
| 4.1.2 | A | Name, role, value |
| 4.1.3 | AA | Status messages |

This is a working subset, not the full standard. The authoritative text is the W3C WCAG 2.2 Recommendation. (SC 4.1.1 Parsing was removed in WCAG 2.2.)

## 11. How to verify, and how to report

Methods, in rough order of cost:

1. **Contrast math:** `python3 scripts/contrast.py FG BG` or `--pairs file`. Verifies color only.
2. **Keyboard pass:** Tab through the whole screen; check order, focus visibility, traps, and that every action is reachable; operate menus, dialogs, and widgets with the keyboard.
3. **Zoom/reflow pass:** 200% browser zoom and a 320px-wide viewport (or 400% zoom); check for clipping and two-way scroll.
4. **Reduced motion pass:** enable the OS setting or emulate it in devtools; check that motion is removed or tamed.
5. **Automated scan** (e.g. axe-core, Lighthouse, or the project's own a11y tests): finds only a subset of issues (commonly estimated at roughly a third); a clean scan is not conformance.
6. **Screen reader spot check** (VoiceOver, NVDA, TalkBack): headings, landmarks, names, states, form errors, dialogs.
7. **Real users with disabilities**, where the product warrants it.

**Report honestly.** Use wording like:

> Checked: contrast of 24 token pairs (script), keyboard pass on the signup screen, 320px reflow. Not checked: screen reader behavior, automated scan, the checkout flow. Findings: 2 behavioral issues reported, not changed (focus not returned after closing the dialog; error summary missing).

Never write "fully accessible", "WCAG compliant", or "passes AA" unless an actual conformance evaluation backs it.
