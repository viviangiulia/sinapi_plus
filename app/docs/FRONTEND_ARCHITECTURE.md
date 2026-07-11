# SINAPI+ — Frontend Architecture

## Initial stack

- React
- TypeScript
- Vite
- React Router
- TanStack Query
- Tailwind CSS
- shadcn/ui
- Lucide React

Do not add Zustand or another global state library unless a concrete need is
identified.

## State strategy

Use:

- React local state for local UI state;
- URL state for navigation-relevant state;
- TanStack Query for server state when backend integration begins;
- a focused theme provider for light/dark/system theme preference.

Do not introduce global state preemptively.

## Initial mode

The first frontend iteration uses mock data.

No backend integration is required unless explicitly requested.

Mock data should be isolated so it can later be replaced by API calls without
rewriting UI components.

## Recommended source structure

src/
├── app/
│   ├── router/
│   ├── providers/
│   └── layouts/
│
├── components/
│   ├── ui/
│   └── shared/
│
├── features/
│   ├── auth/
│   ├── estimates/
│   ├── price-database/
│   └── settings/
│
├── pages/
│
├── mocks/
│
├── lib/
│
├── types/
│
└── styles/

## Architectural principles

### Feature-oriented organization

Business-specific frontend code belongs in feature modules.

Avoid placing all components in one global components directory.

### Reuse intentionally

Extract shared components only when reuse is real or clearly imminent.

Do not create premature generic abstractions.

### Keep domain logic out of visual components

Visual components should not contain complex business calculations.

Future pricing and cost calculation rules belong primarily to the Python
backend.

The frontend may calculate mock totals for prototype demonstration only.

### Separate mock data from UI

Never embed large mock datasets directly inside page components.

### No premature API layer complexity

Do not create speculative abstractions for APIs that do not yet exist.

When integration begins, define a small explicit API client layer.

## Routing concept

Suggested routes:

- `/login`
- `/`
- `/orcamentos`
- `/orcamentos/:id`
- `/base-precos`
- `/configuracoes`

Future:

- `/composicoes`
- `/composicoes/:id`

## Authentication

Initial authentication is mock-only.

The login page exists to validate visual design and navigation flow.

Do not implement real authentication, tokens, sessions, OAuth, or authorization
unless explicitly requested.

## Estimate editor

The estimate editor is the primary workspace.

Initial capabilities:

- display estimate context;
- display total;
- create category;
- rename category;
- collapse/expand category;
- add composition through searchable selector;
- edit quantity;
- remove item;
- calculate mock subtotal and total.

Do not implement composition creation or composition editing in the initial
prototype.

## Accessibility

Use semantic HTML.

All interactive controls must be keyboard accessible where practical.

Provide visible focus states.

Use proper labels for form fields.

Dialogs and popovers should use accessible primitives from the chosen component
system.

## Responsive scope

Initial prototype is desktop-only.

Do not spend implementation effort on mobile or tablet layouts unless
explicitly requested.

Avoid deliberately breaking smaller screens, but full responsive support is
outside scope.

## Dependency policy

Do not add dependencies without a concrete requirement.

Prefer existing stack capabilities.

Before adding a dependency, explain:

- the problem it solves;
- why existing dependencies are insufficient;
- maintenance implications.

## Quality checks

Before considering a task complete:

- TypeScript must compile;
- lint should pass when configured;
- no obvious console errors;
- no unused code introduced;
- no unrelated refactors;
- behavior must match task acceptance criteria.