---
name: anti-slop-ui
description: Design guidance and workflows for improving the visual layer of frontend interfaces so they look intentionally designed rather than generic or AI-generated. Use when asked to build, redesign, refine, polish, audit, or fix the look of UI (components, pages, dashboards, landing pages, forms, onboarding, mobile screens), to remove generic "AI slop" visuals, to review a UI's visual or accessibility quality, or when the user shares screenshots or sites as design references. Adapts to the user's brand and chosen style (minimal, colorful, playful, editorial, maximalist, dark, and more) and runs a short design intake before large work. Changes presentation only (styling, layout, tokens, visual motion) and never alters application behavior without explicit permission. Not for backend, business-logic, data, or other non-visual tasks.
license: No license chosen yet - see README.md
metadata:
  version: "0.2.0"
  status: "pre-release: scripts tested; agent behavior not independently tested (see tests/scenarios.md)"
---

# Anti-Slop UI

Make interfaces that look like a skilled product designer made deliberate decisions for *this* product and *this* audience, not like a template that anyone could have produced.

## 1. The principle

**Adapt to the user. Do not make the user adapt to this skill.**

- "Slop" is a *decision made by default, for no reason*. It is not a color, a gradient, a card, or an animation. A bold gradient with a reason is design. A gray card grid with no reason is slop.
- The goal is to eliminate **generic** design, not **creative** design. Colorful, expressive, maximalist, playful, glassy, animated, and dense interfaces are all valid when intentional and suited to the product.
- Minimalism is one style among many, not a synonym for quality. Never push a project toward black-and-white, grayscale, small type, or "SaaS minimal" unless that is what suits it or what the user wants.
- Behave like a good product designer: understand the product, ask the right questions, propose a direction, respect the user's decisions, and never break what already works.

## 2. How strongly each rule binds

Every rule in this skill carries one of three tags.

| Tag | Meaning | Can the user override it? |
|---|---|---|
| **[MUST]** | Safety, honesty, and accessibility floors. Few and objective. | Only the user, explicitly, and only where noted. |
| **[DEFAULT]** | A sensible starting point when nothing else is specified. | Yes, by the user's preferences, the brand, the existing system, or product context. |
| **[CONTEXT]** | Depends on the product, audience, and style. Decide, and say why. | It is a judgment call, not a rule. |

Untagged guidance is [DEFAULT]. When two rules conflict, apply the order of precedence in section 6.

## 3. When to use this skill

Use it when the user wants to build, restyle, refine, polish, audit, or fix the visual quality of a frontend interface, or supplies design references. Typical triggers: "make this look better / more premium / less generic", "redesign this page", "polish this component", "audit this UI", "fix the mobile layout", "build a landing page / dashboard / onboarding flow".

Do **not** use it for backend work, business logic, data modeling, API design, performance engineering, or any task where the visual layer is not the subject. If a request mixes visual and functional work, apply this skill only to the visual part and follow section 5.

## 4. Step 0: classify the task

Pick one workflow (details in `references/workflows.md`). If unclear, ask one short question.

| Task | Workflow | Design intake | May edit files? |
|---|---|---|---|
| Create a new interface | Build new UI | Full (5-8 questions) + brief + approval, unless the spec is already detailed | Yes, after approval |
| Change the visual direction of an existing UI | Redesign | Full + brief + **approval required** | Only after approval |
| Improve an existing UI while keeping its identity | Refine | Short (1-4 questions) | Yes |
| Review an existing UI | Audit | None (scope only) | **No**, unless implementation is requested |
| Remove generic-looking patterns | Fix AI slop | Short; preserve identity | Yes |
| Improve one component | Component polish | 0-2 questions | Yes, that component only |
| Make it work on small/large screens | Responsive improvement | 0-2 questions | Yes |
| Fix a specific visual defect | Visual bug fix | None | Yes, minimal |

## 5. Visual-only policy [MUST]

The default scope is **visual changes only**. Improve how it looks. Do not silently change what it does.

**Allowed without asking:** CSS and styling, utility classes, design tokens, typography, color, spacing, layout and alignment, borders, surfaces, shadows, component appearance, responsive styling, visual animation and transitions, icon/illustration swaps that do not change meaning or behavior.

**Allowed but disclose in the report** (ask first if the change is large): wrapper or layout markup that leaves handlers and props untouched; swapping one element for a semantic equivalent while preserving every handler and attribute; additive accessibility attributes (`aria-label`, `alt`, `lang`); adding a font, icon, or animation dependency (prefer what the project already has; adding one edits `package.json`, so ask first); edits to visible copy (default: do not rewrite the user's copy for existing UI; mark placeholder copy for new UI as placeholder).

**Forbidden without explicit permission:** business logic; state and hook behavior; event handlers and click behavior; navigation and routing; API calls and data fetching; backend, database, and authentication code; form submission and validation logic; application workflows; component props and contracts; existing integrations; application configuration unrelated to visual design.

Also: never delete working functionality to make a screenshot cleaner, never hide a working control with CSS to simplify a layout, and never replace real components with static mockups.

**Conflict protocol.** If a visual request cannot be met without a functional change, stop that part. Say what conflicts and why, offer a visual-only alternative, and ask before proceeding. Do the rest of the visual work meanwhile.

**Mandatory final diff review.** Before reporting completion, review the full `git diff` and confirm that handlers, state, routes, API calls, forms, and prop contracts are intact. Run `scripts/diff_guard.py` when Python and git are available; it is a heuristic aid, not proof. Details in section 11.

## 6. Respect what exists [MUST]

Precedence, highest first:

1. The user's explicit instruction in this conversation.
2. The approved design brief.
3. The project's existing coherent design system, tokens, and brand identity.
4. User-supplied references (screenshots, URLs), interpreted as principles, not copied.
5. The project's technical conventions (framework, styling approach, component library).
6. This skill's defaults and presets.

Never overwrite a coherent existing design system or brand identity without approval. If the existing system is incoherent (conflicting values, no tokens), say so in the audit/brief and propose consolidation instead of silently imposing a new one. Follow the project's stack; do not introduce React, Tailwind, or a component library the project does not use.

## 7. Design intake

Full guidance and the question bank: `references/design-intake.md`.

**When.** Substantial work: new interface, page, redesign, or major refinement. Not for small, explicitly specified visual fixes (e.g. "make this button 40px tall and use our brand blue", "fix the overflow on mobile").

**How.**
- Ask about 5-8 relevant questions for substantial work, fewer for smaller work, none for explicit fixes.
- Skip any question whose answer is already available: in the request, the conversation, the repository (tokens, config, existing styles, brand assets), attached references, or stored project notes.
- Cover, as relevant: what is being built or improved; product type and audience; visual style; light, dark, or both; color and brand; typography; layout and density; motion; references or inspiration; what to preserve; what the user dislikes; how much creative freedom the agent has.
- Offer example directions (see `references/styles-catalog.md`) but **always allow**: picking one, combining several, describing their own, skipping a question, "you decide", and "keep my current choices". Use the environment's tappable-choice UI if there is one; otherwise a short numbered list. Group questions; do not drip them one by one.
- If the user skips or says "you decide", choose, state the choice in the brief, and continue.

**Brief.** After intake, write a short design brief (template in `references/design-intake.md`): goal, direction, palette and roles, type, layout, motion, **what will change**, **what stays unchanged** (functionality always does, by section 5), assumptions, verification plan.

**Approval.** Get the user's agreement on the brief before starting a **redesign** or other substantial restyle. For a new build, ask for approval too unless the user said to go ahead or "you decide"; then state assumptions and proceed. If the agent cannot ask (non-interactive run), do not start a redesign: deliver the brief and a proposal. Refinements and new builds may proceed on stated assumptions, preserving the existing identity.

## 8. Choosing a visual direction

Decide from context, not habit. Inputs: product category, audience and their context of use, brand identity, user preferences, existing design system, supplied references, and the interface's purpose (a trading terminal, a children's game, and a law firm's site should not look related).

- Pick a direction from `references/styles-catalog.md` or compose one. Combining styles is fine; say which parts come from which.
- Start tokens from `references/tokens.md`. The presets are **starting points**, not requirements. Adapt palette, type, shape, and motion to the direction. Map onto existing tokens if they exist.
- Every hue, typeface, radius, and effect needs a stated role. "It looks modern" is not a role.
- Give the interface a recognizable point of view: one or two deliberate, ownable choices (a type pairing, a color, a shape language, a motion character) executed consistently.

## 9. Main implementation workflow

1. **Classify** the task (section 4) and read the matching workflow in `references/workflows.md`.
2. **Read the project.** Framework, styling system, tokens, components, themes, existing dependencies, git state. Prefer working on a branch or from a clean commit so the diff is reviewable.
3. **Capture a baseline** if tools allow: screenshots of the affected screens at desktop, tablet, and mobile widths, plus key states. See `references/visual-qa.md`.
4. **Intake and brief** (section 7) when the task level requires it.
5. **Analyze references** if supplied (`references/reference-analysis.md`): extract principles, preserve brand identity, never copy.
6. **Plan** before editing: purpose of the screen, primary user action, information hierarchy, layout, emphasis, color roles, responsive plan, real content shapes.
7. **Implement** in the project's own idiom (`references/implementation.md`), touching only what the scope allows. Build real states (hover, focus-visible, active, disabled, loading, empty, error). Mobile-first responsive behavior (`references/responsive.md`). Accessibility as you go (`references/accessibility.md`).
8. **Self-review** against `references/anti-slop-patterns.md` as a judgment aid (not a counter) and `references/visual-qa.md`.
9. **Verify** (section 11). Fix what you find. Re-check.
10. **Report** (section 12).

## 10. Anti-slop as judgment

`references/anti-slop-patterns.md` lists patterns that often signal generic output (random purple-blue gradients, excess glassmorphism, floating orbs, repeated feature cards, generic SaaS heroes, decorative icons, fake statistics, boilerplate copy, shadow overuse, inconsistent type, gratuitous animation, and more). None is automatically bad. For each, ask:

- **Purpose:** what does it do for the user or the brand?
- **Fit:** does it express *this* product and audience?
- **Consistency:** is it applied systematically?
- **Cost:** what does it cost in legibility, performance, or accessibility?

Do not count gradients, cards, or colors and declare a design good or bad. Judge decisions.

Two items stay [MUST] because they are about honesty, not taste: do not invent fake metrics, testimonials, customer logos, or reviews and present them as real (mark placeholders as placeholders); and do not sacrifice legibility or accessibility floors for aesthetics.

## 11. Verification and honesty [MUST]

Before saying a task is done:

1. **Diff review.** Read the full `git diff`. Confirm event handlers, state and hooks, routes, API calls, form attributes and validation, and prop contracts are intact. Run `python3 scripts/diff_guard.py` (if available) and explain every HIGH and REVIEW finding.
2. **Project checks.** Run the project's own type-check, lint, tests, and build if they exist and you can. Report results.
3. **Visual check.** If you can run the app and capture screenshots, inspect desktop, tablet, and mobile, compare with the baseline, fix, and re-check.
4. **Accessibility check.** Run the checks you can (contrast with `scripts/contrast.py`, keyboard pass, zoom/reflow, automated scanner). State which you ran.

**Never claim something was verified when it was not.** Never say "WCAG compliant", "tested on mobile", "build passes", or "no functional changes" without having done the work that supports it. Use the verification ledger in `references/visual-qa.md`: list what was verified, how, and what was not verified.

## 12. Report format

End every task with a concise report:

- What changed (files and a one-line summary each) and what deliberately did not.
- Direction and key decisions, with reasons.
- Visual-only confirmation: diff review outcome and any disclosed gray-zone changes.
- Verification ledger: verified / not verified.
- Open issues and suggested follow-ups. For audits, use the severity-structured report in `references/visual-qa.md` and change no code.

## 13. Reference map

| File | Read when |
|---|---|
| `references/workflows.md` | Starting any task (per-workflow steps, scope, outputs) |
| `references/design-intake.md` | Substantial work: question bank, example directions, brief template, approval |
| `references/styles-catalog.md` | Choosing or combining a visual direction |
| `references/tokens.md` | Setting up or mapping tokens; presets; resolved rule conflicts |
| `references/components.md` | Designing or polishing components |
| `references/implementation.md` | Writing code (frameworks, Tailwind v3/v4, CSS variables, verified examples) |
| `references/responsive.md` | Layouts across screen sizes |
| `references/accessibility.md` | Any UI work (WCAG 2.2 AA target, forms, motion, RTL) |
| `references/reference-analysis.md` | User supplied screenshots or sites |
| `references/anti-slop-patterns.md` | Self-review and fixing generic-looking output |
| `references/visual-qa.md` | Screenshots, severity reports, audits, verification ledger |
| `references/provenance.md` | Questions about where the defaults come from and their limits |
| `scripts/diff_guard.py`, `scripts/contrast.py` | Diff review and contrast checks |
