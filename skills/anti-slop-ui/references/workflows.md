# Workflows

Eight distinct workflows. Each states when to use it, how much may change, the steps, the output, and when it is done. All of them obey the visual-only policy in `SKILL.md` section 5 and the verification rules in section 11.

## Contents
- Shared pre-flight and post-flight
- W1 Build new UI
- W2 Redesign an existing UI
- W3 Refine an existing UI
- W4 Audit an existing UI
- W5 Fix AI-generated visual slop
- W6 Polish an individual component
- W7 Improve responsive layouts
- W8 Fix a visual bug
- Scope boundaries at a glance

---

## Shared pre-flight (all workflows that edit code)

1. **Read the project:** framework, styling approach (Tailwind version, CSS modules, CSS-in-JS, plain CSS), token files, component library, theme mechanism, dependency list.
2. **Check git state.** Note uncommitted work. Prefer a clean commit or a new branch so the final diff contains only this task. If the tree is dirty with unrelated changes, tell the user before proceeding.
3. **Find the baseline:** run the app if possible and capture "before" screenshots (desktop, tablet, mobile; key states). If you cannot run it, say so and work from the code.
4. **Identify behavior-bearing code in the files you will touch** (handlers, state, effects, fetches, routes, forms, props). Treat it as read-only.

## Shared post-flight (all workflows that edit code)

1. Review the full `git diff`.
2. Run `python3 scripts/diff_guard.py` if available and explain every HIGH/REVIEW finding or revert it.
3. Run the project's type-check, lint, tests, and build if available.
4. Capture "after" screenshots and compare, if possible.
5. Write the report with a verification ledger (`visual-qa.md`).

---

## W1. Build new UI

**Use when:** the user wants a new component, page, flow, or app screen.
**May change:** new files and new styling. Existing files only as needed to mount the new UI, and then only per the visual-only policy; wiring a new screen into routing or data is functional work: ask first, or deliver the screen with clearly marked integration points.
**Intake:** full unless the spec is already detailed.

Steps:
1. Intake, brief, approval (`design-intake.md`).
2. Plan: purpose, primary action, information hierarchy, layout, emphasis, color roles, responsive plan, real content shapes. Do not default to a hero + three cards + CTA band; include sections only when the product needs them and real content exists.
3. Set up tokens by mapping to the project's system, or creating a minimal set if none exists (`tokens.md`).
4. Build structure first (semantic HTML, layout, hierarchy) with neutral styling; add brand color, type personality, and effects next.
5. Implement all states and responsive behavior; accessibility as you go.
6. Use realistic content; clearly mark placeholders; no fake metrics/testimonials/logos presented as real.
7. Post-flight.

**Output:** the new UI, the brief, and a report listing any integration points left for the user.
**Done when:** it matches the approved brief, states and breakpoints work, checks run per the ledger.

## W2. Redesign an existing UI

**Use when:** the user wants a different visual direction for existing screens.
**May change:** the visual layer, after approval, including layout structure and color. **Not** behavior.
**Intake:** full, plus explicit "what to preserve". Approval is required before editing.

Steps:
1. Audit the current UI quickly (W4 style, short) to know what exists: tokens, components, inconsistencies, brand elements, behavior-bearing code.
2. Intake and brief. The brief must list what changes and what stays, and state that all functionality stays.
3. Get approval. Do not edit before it.
4. Change tokens first (single source of truth), then shared components, then screens, in that order. This keeps the diff coherent.
5. Keep every handler, state variable, route, fetch, form, and prop contract. If the new layout seems to need a functional change, use the conflict protocol.
6. Post-flight with screenshots before/after.

**Output:** redesigned UI, before/after captures if possible, report.
**Done when:** the new direction is applied consistently, nothing functional changed (diff review clean or explained), approved brief satisfied.

## W3. Refine an existing UI

**Use when:** "make it better / cleaner / more polished" while keeping the product's identity.
**May change:** spacing, hierarchy, typography details, color usage within the existing palette, states, consistency, responsive issues. Not the overall direction, brand, or layout concept.
**Intake:** short.

Steps:
1. Learn the existing identity from tokens, components, and screenshots. Write down its characteristics in 3-5 bullets (palette roles, type, shape language, density).
2. List refinements by impact; fix inconsistencies first (radii, spacing, type scale, states), then hierarchy, then polish.
3. Preserve the identity: if the UI is colorful, stay colorful; if it is dense, stay dense.
4. Post-flight.

**Output:** refined UI + short list of what was improved and why.
**Done when:** the product still looks like itself, only more intentional.

## W4. Audit an existing UI

**Use when:** the user asks for a review, critique, or assessment.
**May change:** **nothing** unless the user asks for implementation afterward.
**Intake:** none; confirm scope (which screens/flows) if unclear.

Steps:
1. Inspect the running app if possible (screenshots at three widths and key states), otherwise inspect code and any provided images; say which.
2. Evaluate three **separate** tracks: functional observations (anything that looks broken or inconsistent in behavior; report, do not fix), accessibility, and visual quality.
3. Report findings with severity (Critical/High/Medium/Low), each with affected element, evidence, impact, and recommended fix (`visual-qa.md`).
4. Include what works well, so strengths are preserved.
5. End with a verification ledger of what was and was not checked.

**Output:** the structured report. No code changes, no commits.
**Done when:** all three tracks are covered and every finding has evidence.

## W5. Fix AI-generated visual slop

**Use when:** the UI looks generic or machine-made and the user wants that fixed.
**May change:** visual layer only, preserving the product's functionality and (unless approved otherwise) its brand.
**Intake:** short: what feels generic, keep brand/layout?, how bold.

Steps:
1. Diagnose using `anti-slop-patterns.md` as a *judgment aid*: for each suspected pattern, ask purpose, fit, consistency, cost. Do not count and condemn.
2. Separate **intentional** choices (keep) from **default-without-reason** choices (replace).
3. Replace with decisions grounded in the product: real content shapes, a typographic point of view, a color system with roles, consistent shape language, purposeful motion.
4. Keep creative elements that serve the brand even if they match a "slop" pattern.
5. Post-flight.

**Output:** improved UI plus a short diagnosis: pattern, verdict (keep/replace), reason.
**Done when:** the interface reads as specific to its product, and every retained or new flourish has a reason.

## W6. Polish an individual component

**Use when:** one component needs visual refinement.
**May change:** that component's styling, and its tokens if shared tokens are insufficient (flag that tokens affect other components). **Not** surrounding components.
**Intake:** 0-2 questions.

Steps:
1. Read the component and where it is used. List its states and variants.
2. Check against `components.md`: hierarchy, spacing, states (hover, focus-visible, active, disabled, loading, error), touch target, contrast, keyboard behavior.
3. Edit only that component's styles. If a change would alter siblings (shared class, shared token), either scope it or disclose the blast radius.
4. Verify all variants and states, not only the default.

**Output:** polished component, list of states checked.
**Done when:** every state and variant looks intentional, and no unrelated component changed.

## W7. Improve responsive layouts

**Use when:** layouts break or feel cramped/empty at some widths.
**May change:** layout CSS, breakpoints, spacing, type scaling, how navigation and tables present at each size. Showing/hiding is allowed only when equivalent access to the content/controls remains; never hide a working control to simplify a layout.
**Intake:** 0-2 questions (target devices, priority breakpoints).

Steps:
1. Reproduce: capture at 320, 375, 768, 1024, 1440 widths (or as available).
2. Work mobile-first (`responsive.md`): fix the narrow layout, then add width-based enhancements.
3. Adapt layouts rather than shrinking them: stack, reflow, change navigation form, convert tables, scroll inside containers.
4. Check touch targets, reflow at 320px / 400% zoom, text spacing overrides, long strings, and RTL if applicable.

**Output:** responsive fixes and a table of widths checked.
**Done when:** no horizontal page scroll (except deliberate data regions), controls reachable and large enough, content readable at each checked width.

## W8. Fix a visual bug

**Use when:** a specific visual defect is reported (misalignment, overflow, wrong color, clipped text, z-index issue).
**May change:** the minimum CSS needed. **No refactors, no redesign.**
**Intake:** none.

Steps:
1. Reproduce and capture evidence (screenshot or computed styles).
2. Find the root cause (inspect cascade, specificity, box model, overflow, stacking context).
3. Fix at the root with the smallest change; do not paper over with `!important` unless the project already relies on it.
4. Check neighboring components and other breakpoints for regressions.

**Output:** the fix, the cause in one or two sentences, what you checked.
**Done when:** the defect is gone at the reported conditions and nothing adjacent regressed.

---

## Scope boundaries at a glance

| Workflow | Changes direction? | Changes layout structure? | Touches other components? | Edits code by default? |
|---|---|---|---|---|
| W1 Build new | n/a (creates) | yes (new) | only to mount, disclosed | yes, after approval |
| W2 Redesign | **yes, after approval** | yes | yes (visual layer) | after approval |
| W3 Refine | no | minor | only for consistency | yes |
| W4 Audit | no | no | no | **no** |
| W5 Fix slop | only where the pattern was a default | as needed | as needed | yes |
| W6 Polish component | no | no | **no** (disclose shared-token impact) | yes |
| W7 Responsive | no | at breakpoints | as needed | yes |
| W8 Visual bug | no | no | no | yes, minimal |
