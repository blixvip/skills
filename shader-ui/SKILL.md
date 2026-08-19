---
name: shader-ui
description: "Integrate tasteful, localized shaders into UI without overwhelming the interface. Use for shader accents, animated fills, edge lighting, corner effects, liquid glass, WebGL backgrounds, and interactive GPU effects. Prefer subtle component-level enhancement over large decorative canvases. Complete within the active /1–/5 timebox or under 10 minutes by default."
---

# Shader Pass

Add shaders as a material and interaction layer, not decoration covering the entire product. Make the result feel polished and intentional. Prefer effects inside edges, corners, borders, fills, hover states, selected states, and small focal surfaces.

## Core principle

A good UI shader is often noticed indirectly. It should make a component feel more responsive, premium, dimensional, branded, or easier to notice. It should not become the main thing the user sees unless the page is intentionally a visual landing page.

When uncertain, reduce the area, opacity, saturation, movement, and number of effects.

## Timebox

Respect the active `/1`–`/5` timebox. When none is active, target completion in under 10 minutes. Shortlist no more than three effects and implement only the strongest one or two.

## Approved sources

Use official code and documentation from the source that best fits the project:

1. Paper Shaders — default for textures, gradients, masked shapes, and restrained accents.
2. Canvas UI — interactive effects over live UI.
3. Liquid Glass JS — glass, refraction, pills, panels, and floating controls.
4. ShaderLabs — hero and section backgrounds.
5. shader-web-background — custom GLSL backgrounds when its license fits.
6. Aladino — effects mapped to individual DOM elements.
7. Svader — Svelte shader components.
8. React Shader — advanced React or WebGPU effects with fallback support.
9. Shaderlib — low-level GLSL utilities when existing components do not fit.

Filter libraries by the project’s framework and avoid unnecessary rendering dependencies.

## Preferred integration patterns

Prioritize shader placement in this order:

### 1. Micro accents

Use shaders in small, controlled areas such as button edges, active borders, card corners, icon backgrounds, input focus rings, selected tabs, progress indicators, avatar rings, small badges, and hover highlights. This is the safest default.

### 2. Component materials

Apply a shader to one important component, such as a featured card, command palette, floating toolbar, modal header, media player, navigation pill, or primary call-to-action. Clip the effect to the component and inherit its border radius.

### 3. Section atmosphere

Use a larger shader only when a section benefits from atmosphere, such as a hero, onboarding screen, empty state, loading experience, or branded landing section. Keep it behind content, low contrast, and visually quiet. Do not default to a giant full-screen shader.

## Good shader treatments

Prefer a glow entering from one corner; slow color movement inside a button border; subtle refraction along a glass-panel edge; masked texture near the perimeter; a shader that strengthens on hover; a small animated fill behind an active icon; a faint moving highlight across a selected card; a restrained light bloom behind one focal element; a shader revealed through a logo or short heading; or a brief ripple or distortion after interaction.

Use shaders to reinforce an existing boundary or interaction.

## Avoid

Do not create huge animated blobs behind every screen, several competing full-screen canvases, brand-unrelated rainbow effects, constant fast movement, shaders behind body text/tables/forms, strong distortion around important controls, glowing borders on every component, effects that make everything equally important, effects added only because a library contains them, or shaders that hide weak spacing, hierarchy, or layout.

Do not use shaders to compensate for an unfinished design.

## Visual restraint

Adapt every effect to the existing UI. Match brand colors, light or dark theme, border radius, surface opacity, motion speed, component hierarchy, existing shadows, and highlights. Use the product palette instead of copying demo colors unchanged.

Prefer two or three related colors, low-opacity movement, slow animation, soft transitions, localized masks, and restrained distortion. On hover or focus, increase the effect slightly instead of running it at full intensity permanently.

## Composition rules

- Default to one primary shader moment per screen.
- Add no more than one or two subtle supporting accents.
- Keep the center of text-heavy components calm.
- Place motion near edges, corners, empty space, or interaction zones.
- Preserve clear visual hierarchy.
- Use masking, clipping, and gradients to blend shaders into the surface.
- Let the shader fade naturally rather than ending at a visible rectangular canvas boundary.
- Avoid placing two moving effects directly beside each other.
- Keep decorative effects visually behind labels, icons, and controls.

## Workflow

1. Inspect the framework, design system, page hierarchy, and existing motion.
2. Identify the highest-value surface or interaction.
3. Decide whether the shader should be a micro accent, component material, or section atmosphere.
4. Compare no more than three compatible effects.
5. Choose the smallest implementation that achieves the intended result.
6. Adapt its palette, speed, opacity, density, scale, and distortion.
7. Mask or clip it into the component instead of leaving an obvious canvas rectangle.
8. Add fallbacks and verify the finished result in context.
9. Remove or reduce the effect if it competes with content.

## Implementation rules

For component-level shaders:

- Position the effect inside a stable component wrapper.
- Use `overflow: hidden` and `border-radius: inherit`.
- Place decorative canvases behind content and apply `pointer-events: none`.
- Give the container explicit dimensions.
- Keep labels and controls as accessible DOM.
- Clean up animation frames, observers, listeners, and WebGL contexts.

Use CSS masks, pseudo-elements, or clipped shader layers for border and corner effects when appropriate.

For interaction effects:

- Support hover, focus-visible, active, and selected states.
- Do not rely on hover alone for important feedback.
- Keep transitions brief and predictable.
- Avoid movement that changes component dimensions.

## Performance and accessibility

- Respect `prefers-reduced-motion`.
- Provide a static CSS fallback.
- Pause rendering when offscreen or when the tab is hidden.
- Avoid multiple full-screen canvases.
- Cap device-pixel ratio when necessary.
- Prevent layout shift, clipping, and stacking conflicts.
- Preserve readable contrast and visible focus states.
- Verify WebGL or WebGPU availability before initialization.
- Check package versions and license compatibility.
- For Chrome extensions, isolate styles, prevent duplicate mounts, avoid blocking native controls, and clean up shaders during SPA navigation.

## Final test

Before finishing, confirm the shader has a clear purpose, is appropriately localized, the interface still works without it, content remains readable and clickable, it matches the product rather than a library demo, motion is restrained, mobile and reduced-motion fallbacks work, and no layout, stacking, or performance problems were introduced. Run the relevant build or targeted test.

Finish with:

```
Added:
Placement:
Source:
Why it fits:
Restraint applied:
Performance safeguards:
Fallback:
Verified:
```

If no shader clearly improves the interface, do not force one.
