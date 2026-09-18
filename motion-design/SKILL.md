---
name: motion-design
description: Design the actual frames for motion graphics and generated UI — palette derived from the footage, type pairing, one of five scene archetypes, and the layering order that produces depth instead of flat AI slop. Use when building scenes in Remotion, HyperFrames, After Effects, or any generated-image pipeline (Nano Banana / GPT Image / Seedream), and whenever output "looks AI-generated", "looks flat", "looks like a template", or needs to match a creator's branding.
---

# motion-design

Frames are **designed pages**, not video with text dropped on top. This skill turns a shot plan (see `motion-plan`) into concrete, on-brand compositions.

Read Appendix A before your first frame. Read Appendix B when you need the layout grammar for a specific scene type.

## 1. Derive the palette from the footage — do not invent one

The accent color is **already in the source video**. Sample it; do not pick one.

1. Pull 3–5 frames from the A-roll. Find the strongest non-skin, non-neutral hue — a lamp, a wall wash, a logo, a jacket, a bit of set dressing.
2. That hue is the **accent**.
3. Read the room's exposure. Bright/airy recording → light-tinted variants. Dim/moody recording → deep variants. A dark scene design over bright footage looks pasted on, and vice versa.
4. Build three roles from that one hue:

| Role | Share | What it is |
|---|---|---|
| **Ground** | 60% | The darker (or, in light themes, the off-white) variant. Backgrounds, large fields. |
| **Surface** | 30% | The lighter variant. Cards, panels, secondary text, texture. |
| **Accent** | 10% | The saturated hue itself. One accent word, one icon, one highlight, one CTA. |

The 10% is a ceiling, not a target. Exceeding it is the fastest way to make a frame look cheap.

**Never use pure `#000000` or `#ffffff` as ground.** Tint both toward the accent — `#0b0a0d`, `#faf8f5`. Pure values are the most recognizable generated-output tell there is.

Write the palette down as tokens before designing anything:

```
--ground     #12100e
--ground-2   #1c1917   /* one step up, for layering */
--surface    #e8e2d9
--surface-2  #b8b0a4
--accent     #e8721f
--accent-dim #7a3d10   /* accent at low luminance, for glows/shadows */
```

Every later frame pulls from these five or six values. Introducing a sixth hue mid-video breaks cohesion.

## 2. Type — two families, three roles, one accent word

- **Display / heavy sans** — the load-bearing words. Condensed heavies read best at short-form sizes. Set tight: tracking `-0.02em` to `-0.04em`.
- **Accent serif italic** — exactly one word or short phrase per frame. This is the single highest-leverage move in the whole style; it is what separates designed frames from Canva output.
- **Mono** — numbers, specs, code, UI chrome. Optional but it makes data read as data.

Rules:
- **One accent word per frame.** Not two. The accent word gets the serif italic *and* the accent color *and* the larger size — all three, on one word.
- Body/support copy sits at 35–50% the size of the display line and drops to 50–60% opacity. It is there to be scanned, not read.
- Never leave text pure flat fill. Give display type a subtle vertical gradient (light top → dark bottom, or the reverse over dark grounds). Flat `#fff` text on a gradient is instantly readable as generated.
- Fonts are a brand decision. If the client has one, use it. Otherwise pick once and never mix a third family in.

## 3. Layer in this order — every time

The order is the whole trick. Skipping a layer is why generated frames look flat.

1. **Ground** — a *gradient*, never a solid. Two to four stops, low contrast between them. Add a subtle grid, paper, or noise texture at 8–15% opacity. Add one large soft light-wash blob (blur 200–350px) in the accent at 20–40% opacity, off-center.
2. **Cast shadow** — before the object. A duplicate of the hero shape, filled solid dark, radially blurred away from a consistent light source, at 35–55% opacity. **One light direction for the entire video.** Inconsistent shadow direction between scenes is a top-three slop tell.
3. **Hero object** — one per frame, occupying 30–55% of the frame area, deliberately off-center. Desaturate it toward the palette (a stock red heart in an orange video must be hue-shifted, not left red). Give it an **inner shadow** (distance 0, size 20–60) so it sits *in* the scene rather than on it. Overlay a halftone or grain texture clipped to it, multiply blend, ~50%.
4. **Supporting copy** — placed *around* the hero, some of it **behind** the hero on the z-axis. Text partially occluded by the object is the cheapest, strongest depth cue available.
5. **Depth elements at the edges** — two or three small related objects, cropped by the frame edge, gaussian-blurred 15–30px, at reduced opacity. They are never fully visible and never the subject. They exist to imply the frame is a window into a larger space.
6. **Post** — vignette (~25–50% at a wide angle), a fine noise/grain pass at 3–8%, and a very slight overall blur ramp at the frame edges.

Layers 2, 5, and 6 are the ones AI pipelines skip. They are also the ones doing the most work.

## 4. Composition

- **Off-center by default.** Centered-everything is the default output of every generator; deliberate asymmetry is the counter-signal.
- **Vary the spacing.** Uniform gaps read as a template. Group related elements tight, push unrelated ones far.
- **One focal point.** Ask "where does the eye land first?" If the answer is ambiguous, the frame fails.
- **Face-safe.** When a person is in a panel or crop, bias the crop so the face is centered in the *visible* area with eyes in the upper third. Default `50% 50%` cuts heads off.
- **Let things break the frame.** An object cropped by the edge reads as real; everything fully contained and margined reads as clip-art.

## 5. When generating frames with an image model

Feed it references, not adjectives. Ten to fifteen saved reference images of the target look, then:

1. Generate **one anchor frame** and approve it before anything else.
2. Generate every subsequent frame with the anchor passed as a **reference image** (Nano Banana / GPT Image / Seedream all support this). This is what holds palette, texture, and framing consistent across a video. Prompting each frame independently produces a set that does not belong together — the most common failure in AI-generated video.
3. Name the palette hexes explicitly in every prompt.
4. **Design mockups before animating.** Animation is the expensive step in both time and credits. Approve stills first, always.

## 6. Self-check before you ship a frame

Run Appendix A. If three or more items fail, redesign — do not patch.

## Handoff

Output for each frame: the palette tokens, the archetype used, a layer-by-layer breakdown, and the element z-order. `motion-animate` needs the z-order and the element names to build timing.

---

# Appendix A — Anti-slop checklist


Run before shipping any frame. Three or more failures = redesign, not patch.

## The instant tells

- [ ] Ground is a **gradient or textured field**, not a flat solid.
- [ ] No pure `#000000` or `#ffffff` anywhere. Everything is tinted toward the palette.
- [ ] Hero object casts a **shadow**, and every shadow in the video falls the same direction.
- [ ] The hero has an **inner shadow** so it sits in the scene, not on it.
- [ ] There is a **texture pass** (grain, halftone, paper, grid) somewhere — even at 8%.
- [ ] There are **edge/depth elements**, blurred and cropped by the frame.
- [ ] Something is **occluded** — text behind an object, an object cropped by the edge.
- [ ] Composition is **off-center**. Not symmetric, not centered-stack.
- [ ] Spacing **varies**. Related things are tight, unrelated things are far.
- [ ] Exactly **one accent word**, and it carries color + serif-italic + size together.
- [ ] Display type has a **gradient fill**, not flat.
- [ ] Type is **two families max**, plus mono for data.
- [ ] Accent color is **≤10%** of frame area.
- [ ] There is a **vignette** and a **grain** pass.
- [ ] Any stock image has been **hue-shifted into the palette**, not left at its original color.

## The structural tells

- [ ] Sequential frames **share the palette** — they were generated from one anchor, not prompted independently.
- [ ] Every frame has **one** focal point, and you can name it.
- [ ] Recurring elements (chapter cards, counters) reuse **one design**.
- [ ] Faces in panels are **face-safe** — centered in the visible crop, eyes upper third.
- [ ] Copy on screen is **3–8 words**, not the full spoken sentence.

## The motion tells (see `motion-animate`)

- [ ] Nothing uses **linear easing**.
- [ ] The camera is **never fully static** for more than ~2s.
- [ ] Elements enter **sequentially**, never all at once.
- [ ] Durations across the edit **vary** — no metronomic rhythm.

## What "it looks AI-generated" almost always means

In order of frequency:

1. Flat solid background, no texture, no gradient.
2. No shadows, or shadows in inconsistent directions between shots.
3. Everything centered and evenly spaced.
4. Default fonts at default tracking, flat white fill.
5. Palette drifts between shots because each was prompted from scratch.
6. Every element animates in at the same moment with the same easing.
7. Full sentences on screen instead of compressed supers.

---

# Appendix B — Scene archetypes


Five. Pick one per beat. Do not invent per-beat looks — recurrence is what makes a video feel authored.

---

## 1. Overlay
**Speaker stays on screen; the graphic shares the frame.**

Use for: filler between chapters, holding retention through a transition, light emphasis where the face still matters.

Layouts:
- Lower-third text + icon strip along the bottom third.
- Graphic occupies one vertical half, speaker the other.
- Small UI card floating in a corner with a connector line to the subject.
- Side-by-side object comparison beneath the speaker.

Rules: never cover the face. Keep the graphic under ~40% of frame area. Ground must be transparent or a soft scrim, not a full field — the footage *is* the background.

---

## 2. Full-frame UI
**The whole frame becomes a designed interface or typographic composition.**

Use for: definitions, comparisons, data, single-concept emphasis, product/app moments.

Layouts:
- Text-focused: one large statement, one word highlighted or underlined.
- Two-object comparison, split down the middle with a seam.
- One object + orbiting supporting text.
- Card stack — three panels with icons, staggered in z.
- Chart/graph build with one point circled.

Rules: this is where glass/UI treatments belong. Panel = gradient fill, `border-radius` large (40–90px at 1080 width), 1px light stroke at low opacity, drop shadow with generous softness and low opacity (~7–15%), plus a light-sweep highlight running diagonally. Backdrop-blur the panel over the ground for real glass. Icons inside get the same cast-shadow treatment as heroes.

---

## 3. Illustrated / cinematic
**A rendered scene with a character or environment.**

Use for: stories, personal anecdotes, experiences, emotional beats.

Layouts:
- Single character, environment implied.
- Character *doing* the thing the line describes.
- Character + environment + a short text super on one edge.
- Abstract/mysterious composition for a concept with no literal referent.

Rules: the character must be **interacting** with the environment, not posed in it. Generate from one approved character anchor and reference it in every subsequent shot, or the person changes between cuts. Camera always moves — a static illustrated frame is a still, not a shot.

---

## 4. Dimensional
**A composition built around a 3D or heavily-dimensional element.**

Use for: rare, high-attention moments only. Product reveals, the one stat that matters, the closing frame.

Rules: use sparingly — two or three per long-form video at most. Overuse turns premium into gaudy. Requires the strongest lighting/shadow discipline of any archetype: one key light, consistent direction, real contact shadow where the object meets a surface.

---

## 5. Typographic
**Type is the entire composition.**

Use for: quotes, conclusions, chapter titles, the closing line.

Layouts:
- One statement, mixed weights, one accent word.
- Word-stack with size hierarchy across three or four lines.
- Big background letterform (a word set huge and low-contrast) with small readable text over it.

Rules: this archetype lives or dies on the type pairing and the accent word. Add one graphic element — a rule, a bracket, an underline sweep, a small icon — so it is a designed frame rather than a slide.

---

## Recurring elements

Anything appearing more than once — chapter card, section counter, brand mark, stat frame — gets **one** design, reused with different content. Same archetype, same layout, same motion. Re-designing it each time destroys the viewer's structural map.
