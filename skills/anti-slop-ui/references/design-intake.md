# Design intake

A short, conversational consultation before substantial UI work. Goal: learn what the user wants so the result is theirs, not a default.

## Contents
1. When to run it (and when not to)
2. Rules of the conversation
3. Question bank (pick 5-8)
4. Example visual directions to offer
5. Handling answers: skip, "you decide", preserve, combine
6. Design brief template
7. Approval gate
8. Non-interactive runs
9. Worked examples

---

## 1. When to run it

| Situation | Intake level |
|---|---|
| Explicit, narrowly specified visual fix ("button 40px tall, brand blue", "fix overflow at 375px") | **None.** Just do it. |
| Audit / review only | **None.** Ask only which screens or flows are in scope if unclear. |
| Single component polish, small refinement, responsive fix with no stated direction | **Light:** 1-3 questions, only the unknowns. |
| New page or interface, redesign, major restyle, new design system | **Full:** about 5-8 questions, then a brief, then approval. |

Do not turn a small request into a questionnaire. If in doubt between light and full, ask the two most decision-relevant questions and offer "or tell me to just decide".

## 2. Rules of the conversation

1. **Check what you already know first.** Look in: the user's message and earlier conversation; the repository (tailwind config, CSS variables, theme files, existing components, brand assets, README, design docs); attached screenshots and links; any project notes the user has stored. Do not ask for anything you can read.
2. **Ask only relevant questions.** A database admin tool does not need "which illustration style?".
3. **Ask once, grouped.** Send all questions together (numbered or as choices), not one per turn. Use the environment's tappable-choice UI if available; otherwise a numbered list with short options.
4. **Always allow custom answers.** Every question accepts: one of the offered options, a combination, the user's own words, "skip", "you decide", or "keep what I have".
5. **Offer examples, not a menu of rules.** Options illustrate; they do not limit.
6. **Be concrete.** "Colorful" is vague; "muted brand blue with one warm accent" or "vivid, multi-color, playful" is answerable. Offer a short phrase of what each option means.
7. **Do not lead toward minimalism or monochrome.** Present colorful, expressive, and dense options with the same weight as restrained ones.
8. **Stay in character.** Sound like a product designer: brief, curious, specific.

## 3. Question bank

Pick the 5-8 that are relevant and still unknown. Each lists what it is for and example options. Always append: *"...or describe your own / skip / you decide."*

1. **Goal and scope.** What are we building or improving, which screens or components, and what does success look like?
   *e.g. "New pricing page", "restyle the whole dashboard", "polish the settings form".*
2. **Product and audience.** What kind of product, who uses it, in what context (desk, phone, on the move, long sessions), any age, expertise, language, or regional needs (RTL, CJK)?
3. **Visual direction.** Which of these feels closest? (see section 4) Combine freely.
4. **Theme.** Light, dark, both with a toggle, or follow the system? Is there an existing theme to keep?
5. **Color and brand.** Existing brand colors or logo to match? Colors to use or avoid? How colorful: restrained, balanced, vivid? Are gradients welcome?
6. **Typography.** Existing fonts? Mood: neutral sans, geometric, humanist, serif/editorial, monospace, expressive display? Any font-loading or licensing limits?
7. **Layout and density.** Compact and information-dense, balanced, or airy? Structure preferences (sidebar app shell, centered column, editorial grid, full-bleed)?
8. **Motion and interaction.** None, subtle and fast, or expressive (springs, scroll effects, page transitions)? Any motion-sensitivity or performance constraints?
9. **References and inspiration.** Sites, apps, or screenshots you like, and *what specifically* you like about each (color, type, spacing, feel)?
10. **Preserve.** What must not change: brand, layout, copy, specific components, behavior? (Behavior never changes by default; see the visual-only policy.)
11. **Dislikes.** Styles, colors, patterns, or effects you want to avoid?
12. **Creative freedom.** Conservative (match what exists), moderate (improve within the current identity), or high (propose something bolder)?

Optional constraint questions when relevant: framework and component library in use; accessibility target beyond the default; browsers/devices to support; may the agent add a font, icon set, or animation dependency; may visible copy be rewritten.

## 4. Example visual directions to offer

Keep each to a short phrase. Full detail is in `styles-catalog.md`.

- **Precise neutral**: tight, quiet, tool-like; layered grays with one accent.
- **Warm and friendly commerce**: warm neutrals, strong brand color, product-forward.
- **Playful and bright**: saturated colors, chunky shapes, personality.
- **Editorial**: serif or high-contrast type, strong grid, paper-and-ink feel.
- **Dark developer tool**: deep dark surfaces, mono accents, high information density.
- **Expressive gradient / glass**: gradients, blur, and glow used deliberately for a consumer or media product.
- **Neo-brutalist**: flat color, thick borders, hard shadows, raw type.
- **Soft and calm (health, finance)**: gentle color, rounded forms, reassuring.
- **Luxury / premium**: restrained palette, generous space, refined type.
- **Maximalist / creative portfolio**: oversized type, asymmetry, rich motion and imagery.
- **Enterprise calm**: dense, clear, data-first, conservative color.
- **Retro / nostalgic**: pixel, Y2K, print, or terminal throwbacks.

## 5. Handling answers

| User says | Do this |
|---|---|
| Picks one direction | Use it; adapt tokens (`tokens.md`); state palette and type roles in the brief |
| Picks several | Combine; state which attributes come from which (e.g. "editorial type and grid, playful color") |
| Describes their own | Translate to concrete attributes (palette, type, shape, density, motion); confirm in the brief |
| Skips a question | Decide sensibly from context; list it as an assumption |
| "You decide" | Decide, explain the choice in one line each in the brief; proceed per the approval rules |
| "Keep what I have" | Preserve the existing choice for that dimension; do not "improve" it |
| Gives conflicting answers | Name the conflict, propose how to reconcile (e.g. vivid accent inside a calm layout), ask only if it changes the outcome |
| Gives a link or screenshot | Follow `reference-analysis.md`; extract principles, never copy |

## 6. Design brief template

Keep it to roughly one screen. Plain language; no jargon the user did not use.

```markdown
## Design brief: <name>

**Goal:** <one sentence>
**Scope:** <screens/components affected>
**Task type:** <build new | redesign | refine | polish | ...>

**Direction:** <named style(s) or the user's own description>, because <reason tied to product/audience>
**Color:** <roles: brand, accent, neutrals, status; light/dark/both>. <Gradients: yes/no and where>
**Typography:** <families or categories; weight/size character>
**Layout & density:** <structure; compact/balanced/airy>
**Motion:** <none/subtle/expressive; what animates and why>
**Responsive:** <how layout adapts, mobile-first notes>

**What will change:** <bullets: visual only>
**What will stay unchanged:** <bullets: brand elements, layout areas, copy, and always: all functionality (handlers, state, routes, API, forms, props)>

**Assumptions:** <anything you decided because the user skipped it>
**Risks / open questions:** <e.g. "new font adds a dependency; OK?">
**How I'll verify:** <diff review, screenshots at 3 widths, contrast check, keyboard pass; what I cannot verify>

Shall I proceed? (yes / change X / just do it your way)
```

## 7. Approval gate

- **Redesign or large restyle:** do not edit until the user agrees to the brief. A reply like "go ahead", "looks good", or "you decide" counts. Silence does not.
- **New build:** ask for agreement unless the user already said to proceed or "you decide"; then state the assumptions and start.
- **Refinement / polish:** a one- or two-line plan is enough; proceed unless the user objects.
- If the user changes direction mid-task, update the brief and re-confirm only if the scope or identity changes materially.

## 8. Non-interactive runs

If the agent cannot ask questions (batch, CI, autonomous run):
- **Redesign:** do not start. Produce the brief and a proposal (and optionally a mock in a separate file or branch) and stop for review.
- **New build or refinement:** proceed with the most conservative reading: preserve the existing identity, use the detected design system, choose a direction suited to the product context, and write all assumptions at the top of the brief and the final report.
- **Audit:** proceed; no code changes.

## 9. Worked examples

**A. "Build a landing page for my coffee subscription."** Known: product type. Ask (grouped): audience and tone; visual direction (warm commerce / editorial / playful / your own); brand colors or logo; light/dark; photography available?; references; anything to avoid; freedom level. That is 7. Then brief, then approval.

**B. "Make this dashboard look less generic."** Known: existing UI in repo. Read tokens and screenshots first. Ask 3-4: what feels generic to you; keep brand colors and layout?; how bold may I go (conservative / moderate / bold); density preference. Brief is short; this is a refinement that preserves identity.

**C. "Make this button primary color #1f6feb with 8px radius."** No intake. Do it, keep the diff minimal.

**D. "Redesign my portfolio. Make it wild."** Ask 5-6: what you do and who you want to impress; directions (maximalist, editorial, neo-brutalist, your own); color appetite; motion appetite; references; must-keep (name, projects, copy). Brief and approval before any edits; behavior (links, forms) stays untouched.
