# SINAPI+ — Product Context

## Product vision

SINAPI+ is a professional web application for creating construction and
infrastructure cost estimates using recognized and reliable cost references,
initially based on SINAPI data.

The product aims to make cost estimation faster, clearer, traceable, and
organized while preserving flexibility for different types of construction
projects.

## Core value proposition

Users can:

- create construction cost estimates;
- define the Brazilian state (UF) used for regional pricing;
- select the price reference source and competence period;
- create custom categories inside an estimate;
- search and add existing cost compositions;
- define quantities;
- automatically calculate subtotals and the total estimate;
- inspect reference compositions and their components;
- export results.

## Core domain concepts

### Estimate

Represents a construction cost estimate.

Initial conceptual fields:

- id
- name
- optional description
- UF
- price reference source
- competence period
- categories
- created_at
- updated_at
- total

### Category

A user-defined organizational group inside an estimate.

Examples:

- Água Potável
- Esgoto Sanitário
- Pavimentação
- Terraplenagem
- Any other name defined by the user

Fields:

- id
- name
- order
- items
- subtotal

Categories are not predefined by the application.

### Estimate item

Represents a composition added to a category.

Fields:

- composition
- quantity
- unit price
- total price

A composition should not be duplicated inside the same category.

### Composition

Represents a cost composition from a recognized reference source or,
in future versions, a custom composition.

Conceptual fields:

- code
- description
- unit
- origin
- components/inputs

The composition price depends on pricing context such as:

- UF
- competence period
- reference source

## Initial product areas

### Login

Mock authentication screen used only to validate the intended future user
experience. No real authentication is required in the initial prototype.

### Home

A clean product entry page.

Do not show recent estimates in the initial prototype.

The page should introduce the product and provide a clear primary action for
creating a new estimate without becoming a documentation-heavy landing page.

### Estimates

Lists and manages estimates.

The initial prototype uses mock data.

Users can create an estimate through a compact modal containing:

- name
- optional description
- UF
- price reference source
- competence period

### Estimate editor

The primary operational workspace of the product.

Users can:

- create categories;
- rename categories;
- collapse and expand categories;
- add compositions through a searchable contextual selector;
- edit item quantities directly;
- remove items;
- see category subtotals;
- see the total estimate.

Category reordering is part of the product model but does not need to be
implemented in the first prototype unless explicitly requested.

### Price database

Allows users to browse and search reference compositions and inputs.

Initial filters may include:

- search by code or description;
- UF;
- competence period;
- item type.

### Settings

Contains user and application preferences, initially using mock data.

## Future vision

Future capabilities may include:

- real authentication and user accounts;
- persistent estimates;
- custom user compositions;
- cloning official compositions;
- editing composition inputs and coefficients;
- reusable custom compositions;
- multiple price reference sources;
- historical price analysis;
- comparison between scenarios;
- PDF and Excel exports;
- collaboration.

These capabilities must not be implemented unless explicitly requested.

## Current scope boundaries

The initial frontend prototype:

- uses mock data;
- has no real backend integration;
- has no real authentication;
- does not create custom compositions;
- targets desktop only;
- does not require mobile or tablet support.

## Terminology

Use "orçamento" as the primary Portuguese product term.

Avoid using "simulação" as a synonym for the core estimate entity.

"Simulação" may eventually represent alternative scenarios within an estimate.