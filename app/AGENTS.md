# AGENTS.md

## Project

SINAPI+ is a professional construction cost-estimation application based on
recognized cost references, initially SINAPI.

The frontend is being developed through AI-assisted development.

## Required context

Read only the documentation relevant to the current task:

- Product/domain behavior: `docs/PRODUCT.md`
- UX and visual decisions: `docs/DESIGN.md`
- Technical architecture: `docs/FRONTEND_ARCHITECTURE.md`

Do not load or restate unrelated documentation.

## Working rules

Before coding:

1. Inspect the existing repository and relevant files.
2. Reuse existing patterns and components.
3. State a short implementation plan for non-trivial tasks.
4. Ask only when ambiguity materially affects the result.

During implementation:

- Keep changes scoped to the requested task.
- Do not perform unrelated refactors.
- Do not add dependencies without justification.
- Do not invent backend APIs.
- Do not implement future features unless requested.
- Preserve strict TypeScript typing.
- Prefer simple code over speculative abstractions.

## Frontend stack

Use the existing project stack:

- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Tailwind CSS
- shadcn/ui
- Lucide React

Do not introduce global state libraries without demonstrated need.

## Design

Follow `docs/DESIGN.md`.

Key constraints:

- Corporate Editorial Engineering aesthetic.
- Desktop-first initial prototype.
- Light, dark, and system themes.
- No generic SaaS visual style.
- No excessive cards, gradients, shadows, radius, or animations.
- Use Lucide icons only.
- Use semantic design tokens. Do not hardcode theme-dependent colors.

## Scope discipline

The initial prototype uses mock data.

Do not implement:

- real authentication;
- real backend integration;
- custom composition creation;
- mobile/tablet optimization;

unless explicitly requested.

## Completion

Before finishing:

- run available type checks;
- run lint if configured;
- report changed files;
- report validation performed;
- mention remaining limitations briefly.