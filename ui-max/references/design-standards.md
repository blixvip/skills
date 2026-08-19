# Production UI Standards

Use this reference during substantial visual implementation, UI cleanup, responsive work, accessibility review, state design, forms, and tables.

## Contents

- [Tokens](#tokens)
- [Layout](#layout)
- [Typography and icons](#typography-and-icons)
- [Motion](#motion)
- [Accessibility](#accessibility)
- [States](#states)
- [Forms](#forms)
- [Tables and lists](#tables-and-lists)
- [Responsive design](#responsive-design)
- [Anti-patterns](#anti-patterns)

## Tokens

Define semantic tokens instead of scattering arbitrary visual values:

```css
--background;
--foreground;
--card;
--card-foreground;
--popover;
--popover-foreground;
--primary;
--primary-foreground;
--secondary;
--secondary-foreground;
--muted;
--muted-foreground;
--accent;
--accent-foreground;
--destructive;
--destructive-foreground;
--border;
--input;
--ring;
--success;
--warning;
--info;
```

Prefer semantic classes:

```tsx
className="border-border bg-card text-card-foreground"
```

Avoid scattered literals such as:

```tsx
className="border-zinc-700 bg-[#121212] text-[#f4f4f5]"
```

Allow hard-coded values only for deliberate brand details or visualizations that cannot be represented semantically.

## Layout

Use a consistent spacing scale:

```text
4px   tiny visual adjustment
8px   tightly related elements
12px  compact controls
16px  standard component spacing
24px  section spacing
32px  major separation
48px+ page-level separation
```

- Keep related controls close and separate unrelated sections clearly.
- Align labels and controls consistently.
- Avoid nested cards, large empty dashboard panels, and excessive padding in browser sidebars.
- Use responsive grids only when items benefit from multiple columns.
- Use lists/tables for comparison. Use cards for heterogeneous, individually actionable items.
- Keep primary actions obvious and destructive actions apart from routine actions.

## Typography and icons

Use one primary interface font unless branding requires otherwise. Prefer Inter, Geist, IBM Plex Sans, or the system stack. For monospace, prefer Geist Mono, JetBrains Mono, IBM Plex Mono, or system monospace.

Build restrained hierarchy with size, weight, color, spacing, and grouping across page titles, section titles, component titles, body, supporting text, labels, and metadata. Do not make everything large or make important status text extremely small.

Use one icon family. Default to Lucide; Phosphor and Heroicons are acceptable alternatives. Do not casually mix families. Keep stroke weights consistent, label unfamiliar icon-only actions with tooltips and accessible names, use icons to support rather than replace labels, avoid decorating every heading, and use filled status symbols sparingly.

## Motion

Use motion to communicate state change, hierarchy, continuity, cause/effect, progress, or focus.

Recommended durations:

```text
100–150ms hover and press
150–250ms menus, tooltips, tabs
200–350ms dialogs, drawers, expanding panels
300–500ms larger layout transitions
```

Use ease-out for entry, ease-in for exit, springs for direct manipulation, and linear easing for continuous progress.

Avoid animating every element on load, long bouncing transitions, excessive glow, competing background animation, delayed interaction, dramatic motion in dense productivity UI, or layout motion that makes text hard to track. Respect `prefers-reduced-motion`.

## Accessibility

Support:

- keyboard operation and logical tab order
- visible focus styles
- semantic controls and input labels
- accessible names for icon buttons
- correct dialog focus management
- sufficient contrast
- screen-reader-readable status messages
- non-color indicators for important state
- reduced-motion preferences

Use `button` or `a` instead of a clickable `div` when semantically appropriate. Never remove outlines without an equivalent visible focus state.

## States

Consider initial loading, background refreshing, empty results, no search matches, success, warning, error, partial failure, disabled, offline, permission required, missing integration, and stale data.

Do not use a spinner as the sole response to every condition. Prefer skeletons when the expected structure is known.

Make errors explain:

1. What failed.
2. Why, when known.
3. Whether user work is preserved.
4. What resolves it.

## Forms

Default substantial React forms to React Hook Form + Zod + shadcn/ui. Avoid needless abstraction for one- or two-field forms.

- Validate on an appropriate schedule.
- Keep errors next to their fields.
- Preserve input after recoverable failures.
- Disable submission only when necessary.
- Show submission progress and prevent duplicate submission.
- Mark optional fields clearly.
- Never use placeholder text as the only label.
- Confirm destructive changes.
- Use appropriate input types and autocomplete attributes.

## Tables and lists

Use TanStack Table only when advanced behavior is necessary: sorting, filtering, pagination, selection, column visibility, pinned columns, virtualization, bulk actions, responsive fallback, or complex data models. Use simple markup for static lists.

Provide empty and loading states. In narrow panels, replace wide tables with compact rows or stacked cards. Never shrink desktop tables until unreadable.

## Responsive design

Test the real target surfaces at minimum where relevant:

```text
320px
375px
768px
1024px
1280px
1440px
```

For browser extensions, also test 320–420 px popups, 320–600 px side panels, and full dashboards. Do not assume desktop layouts work automatically in side panels.

Use progressive disclosure, compact action menus, stacked layouts, text truncation with accessible full-value access, responsive navigation, and sticky controls only when they remain useful.

## Anti-patterns

Never:

- install multiple complete UI frameworks for isolated components
- create conflicting button systems or casually mix icon families
- hard-code colors throughout copied code
- add animation because a library offers it
- apply cinematic effects throughout dashboards
- use cards where compact comparison belongs in a list/table
- hide every action behind icon-only controls
- use giant headers in small extension surfaces
- invent analytics, meaningless mock data, fake agent activity, or nonfunctional controls
- build inaccessible custom dropdowns/dialogs
- substitute gradients and glows for hierarchy
- copy components without mobile review
- treat loading, empty, and error states as afterthoughts
- redesign stable components without a product reason
