# Component Selection Reference

Use this reference when choosing UI sources, evaluating alternatives, installing dependencies, or gathering design inspiration.

## Contents

- [Source priority](#source-priority)
- [Specialized enhancements](#specialized-enhancements)
- [Alternative full systems](#alternative-full-systems)
- [Design-system references](#design-system-references)
- [Inspiration and generation tools](#inspiration-and-generation-tools)
- [Installation, licensing, and ownership](#installation-licensing-and-ownership)
- [Selection matrix](#selection-matrix)

## Source priority

### shadcn/ui

Use [shadcn/ui](https://ui.shadcn.com) as the primary React source for buttons, inputs, forms, dialogs, drawers, menus, selects, tabs, tooltips, popovers, command palettes, sidebars, navigation, tables, cards, toasts, alerts, sheets, context menus, date pickers, and settings controls. Prefer it because the project owns and can customize the copied code.

### Radix UI

Use [Radix UI](https://www.radix-ui.com) directly when shadcn does not expose a needed primitive, custom primitive-level behavior is required, accessibility needs tighter control, or building a reusable design-system component. Do not recreate accessible dialogs, menus, popovers, switches, or tooltips from scratch.

### 21st.dev

Use [21st.dev](https://21st.dev) to discover React/Tailwind components compatible with the shadcn ecosystem, especially dashboards, sidebars, pricing, settings, authentication, empty states, cards, SaaS structures, and AI interfaces.

Treat discovered code as a starting point. Before use:

1. Inspect dependencies and license.
2. Remove unnecessary effects.
3. Convert colors to project tokens.
4. Match spacing and radius scales.
5. Confirm mobile behavior and keyboard accessibility.
6. Remove duplicated utilities.

## Specialized enhancements

### Motion Primitives

Use [Motion Primitives](https://motion-primitives.com) for restrained animated tabs, shared-layout transitions, expandable panels, text transitions, carousels, progressive disclosure, hover interactions, and animated values/status. Prefer it for Linear-, Stripe-, or Vercel-style product motion before cinematic animation libraries.

### Magic UI

Use [Magic UI](https://magicui.design) selectively for marketing heroes, animated borders, beams, marquees, bento grids, backgrounds, logo clouds, and product showcases. Do not apply landing-page effects to every card, button, panel, or settings page.

### Aceternity UI

Use [Aceternity UI](https://ui.aceternity.com) only when cinematic landing pages, 3D cards, spotlights, beams, animated grids, or high-impact showcases serve a real product need. Avoid these effects in dense application interfaces unless they improve comprehension.

### Cult UI

Use [Cult UI](https://cult-ui.com) for actual AI chat layouts, agent activity, streaming responses, tool-call displays, reasoning summaries, prompt composers, model selectors, artifacts, and generative loading states. Do not add fake agent activity, fabricated reasoning, or decorative tool-call animations.

### UIverse

Use [UIverse](https://uiverse.io) only for isolated toggles, loaders, creative buttons, hover effects, or experimental controls. Treat snippets as demonstrations; review accessibility, maintainability, dependencies, and design-system consistency heavily before production use.

## Alternative full systems

Use a full system only when it already exists, the framework requires it, its strengths match real requirements, or replacement would cause unnecessary migration.

### React

- [HeroUI](https://heroui.com): polished general-purpose apps and React Aria-based interactions.
- [Mantine](https://mantine.dev): component-heavy internal tools, dashboards, rich hooks, and rapid development.
- [Material UI](https://mui.com): products intentionally using Material Design or established enterprise MUI codebases.
- [Ant Design](https://ant.design): enterprise and data-heavy administration with complex tables/forms.
- [Chakra UI](https://chakra-ui.com): established Chakra projects and teams using its token/composition model.
- [PrimeReact](https://primereact.org): enterprise apps requiring complex widgets and rich data controls.

### Vue

Use ecosystem-native systems such as PrimeVue, Element Plus, or Quasar. Do not force React libraries into Vue.

### Svelte

Use ecosystem-native systems such as Skeleton, Melt UI, or Bits UI. Do not redesign Svelte around React assumptions.

## Design-system references

Study established patterns without necessarily installing their code:

- [Material Design 3](https://m3.material.io): responsive behavior, interaction states, elevation, navigation, mobile patterns.
- [Fluent 2](https://fluent2.microsoft.design): desktop productivity, Microsoft-style command surfaces, enterprise UI.
- [Atlassian Design System](https://atlassian.design): project management, productivity, issue tracking, data-dense workflows.
- [Shopify Polaris](https://polaris.shopify.com): Shopify embedded applications and commerce administration.
- [Carbon Design System](https://carbondesignsystem.com): complex enterprise and data-heavy products.

## Inspiration and generation tools

Use inspiration to understand patterns, not copy products blindly:

- [Mobbin](https://mobbin.com): real product flows and interface patterns.
- [Dribbble](https://dribbble.com): visual exploration; treat concepts as inspiration, not validated UX.
- [Behance](https://behance.net): case studies and complete visual systems.
- [Awwwards](https://www.awwwards.com): experimental marketing and portfolios; avoid importing heavy animation into productivity tools without reason.

Use AI/design tools to accelerate exploration, never replace engineering judgment:

- [v0](https://v0.dev): React, Tailwind, shadcn-style page/component prototypes. Review accessibility, responsiveness, dependencies, hard-coded colors, duplication, mock data, and states.
- [Builder.io](https://www.builder.io): visual composition and content-managed experiences.
- [Locofy](https://www.locofy.ai): structured Figma-to-code starting points; refactor before production.
- [Figma](https://figma.com): layout, tokens, prototypes, variants, auto-layout, and handoff.
- [Framer](https://framer.com): marketing sites and interactive prototypes.

## Installation, licensing, and ownership

When explaining a resource, provide only what fits the current stack:

1. Why it fits.
2. Installation command.
3. Minimal implementation.
4. Direct documentation link.
5. Dependency or licensing warning.
6. Existing-project integration notes.

Examples:

```bash
npx shadcn@latest add dialog
npm install motion
npm install react-hook-form zod @hookform/resolvers
```

Do not dump commands for competing libraries.

Before copying marketplace/community code, inspect the license, preserve attribution, distinguish free and premium assets, avoid proprietary components without permission, document meaningful third-party code, and review introduced dependencies. Public visibility does not imply unrestricted use.

## Selection matrix

| Requirement | Default choice |
| --- | --- |
| Core application UI | shadcn/ui |
| Accessible primitives | Radix UI |
| Component discovery | 21st.dev |
| Subtle product animation | Motion Primitives |
| General React animation | Motion |
| AI chat and agent UI | Cult UI |
| Marketing effects | Magic UI |
| Cinematic effects | Aceternity UI |
| Advanced data tables | TanStack Table |
| Forms | React Hook Form + Zod |
| Icons | Lucide |
| Existing MUI project | Continue MUI |
| Existing Ant Design project | Continue Ant Design |
| Vue application | Vue-native libraries |
| Svelte application | Svelte-native libraries |
| Product-flow research | Mobbin |
| Fast React prototype | v0 |
| Marketing prototype | Framer |

Default most React product UI to shadcn/ui, Radix UI, Tailwind CSS, Lucide, and Motion only where useful. Add a specialized library only when it solves a specific problem better than the foundation.
