---
name: ui-max
description: Design, improve, clean up, or implement polished production interfaces with coherent component selection, accessibility, responsive behavior, maintainable design tokens, restrained motion, and complete UI states. Use for dashboards, SaaS products, browser extensions, AI tools, admin panels, settings, forms, tables, marketing pages, component libraries, UI audits, and frontend rebuilds where Codex must select the smallest appropriate UI stack and deliver working code.
---

# UI Max

Prioritize product usability over decorative effects. Choose the simplest coherent system that satisfies the requirement; do not accumulate component libraries.

## Start with the product

Before changing code:

1. Inspect the framework, router, CSS system, component library, icon and animation libraries, form stack, design tokens, dark mode, and established patterns.
2. Define the user's goal, primary workflow, information hierarchy, primary and secondary actions, required states, responsive surfaces, and keyboard behavior.
3. Reuse in this order: local components, existing design-system primitives, shadcn/ui, Radix UI, 21st.dev, a specialized enhancement library, custom implementation.
4. Keep an existing stable UI system. Never introduce a competing full system for one attractive component.

## Choose one foundation

For new React product interfaces, default to:

```text
React + TypeScript + Tailwind CSS
shadcn/ui -> Radix UI primitives
Lucide icons
Motion for React only where useful
React Hook Form + Zod for substantial forms
TanStack Table only for advanced table behavior
```

Do not force this stack into projects with an established system or into Vue/Svelte projects. Use ecosystem-native libraries there.

Classify the surface before selecting additions:

- Core product UI: shadcn/ui + Radix UI + Tailwind CSS.
- AI product UI: add Cult UI only for real AI workflow patterns; use Motion Primitives for restrained transitions.
- Marketing page: use 21st.dev for structure, Magic UI selectively, and Aceternity only for genuinely high-impact sections.
- Data-dense application: add TanStack Table when sorting, filtering, pagination, selection, visibility, virtualization, or complex data models justify it.
- Micro-interaction: use Motion Primitives or Motion. Use UIverse only after accessibility and maintainability review.

Read [references/component-selection.md](references/component-selection.md) when choosing, installing, or sourcing libraries/components, comparing alternatives, or researching visual patterns.

## Implement coherently

Normalize every reused or copied component to the project's:

- semantic color tokens
- typography, spacing, radius, and shadow scales
- icon family
- accessibility conventions
- responsive behavior
- light and dark themes

Use semantic tokens rather than scattered hard-coded values. Keep related controls close; separate unrelated sections; avoid unjustified nested cards; use lists/tables for comparison and cards for individually actionable, heterogeneous items. Keep primary actions obvious and destructive actions away from routine actions.

Use one interface font and one icon family unless branding requires otherwise. Use motion only to communicate state, hierarchy, continuity, cause/effect, progress, or focus. Respect `prefers-reduced-motion`.

Read [references/design-standards.md](references/design-standards.md) before substantial visual implementation, responsive work, state design, forms, tables, or accessibility work.

## Cover real states

For asynchronous or data-driven UI, consider:

- initial loading and background refresh
- empty results and no search matches
- success, warning, error, and partial failure
- disabled and offline states
- missing permissions or integrations
- stale data

Prefer skeletons when structure is known. Make errors say what failed, why when known, whether work is preserved, and what resolves it. Never use meaningless mock data, fake analytics, fabricated agent activity, or nonfunctional controls in a finished product.

## Clean up existing UI

Audit duplication, spacing, colors, typography, variants, icons, nested layout, repeated utilities, responsiveness, accessibility, unused code/dependencies, animation overload, and missing states.

Consolidate repeated or behavior-bearing primitives such as buttons, inputs, status badges, dialogs, menus, tabs, page headers, empty/error/loading states, sidebar items, and project rows. Do not abstract one-off markup without a consistency, logic, reuse, or testing benefit.

Tokenize repeated values. Remove unnecessary wrappers, nested cards, decorative dividers, repeated labels, redundant actions/status, excessive descriptions, and unjustified motion.

## Validate rendered output

Verify:

- semantic HTML, accessible names, labels, logical tab order, keyboard operation, dialog focus, visible focus, and contrast
- loading, empty, disabled, error, success, long-text, and destructive-confirmation states
- narrow and wide layouts without clipping, unreadable tables, layout shift, or horizontal overflow
- reduced-motion behavior, light/dark themes, and responsive navigation
- formatter, lint, TypeScript, tests, production build, and console output

Test at 320, 375, 768, 1024, 1280, and 1440 px when relevant. For browser extensions, also test popup widths around 320–420 px and side panels around 320–600 px.

Inspect the actually rendered UI at narrow and wide widths before claiming completion. Use a screenshot loop or the project's existing visual-validation workflow; confirm platform-specific surfaces on the real target.

## Report UI work

When asked to design or rebuild a page, provide concise sections for:

1. Product interpretation: goal, primary workflow, key information, main action.
2. Component plan: structure, reusable components, foundation, specialized additions, responsive behavior, important states.
3. Implementation: working code in the existing stack.
4. Validation: accessibility, responsiveness, states, keyboard behavior, design-token consistency, and rendered visual review.

Do not return a library catalogue unless the user asks for options.
