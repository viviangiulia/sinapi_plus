# SINAPI+ — Design System and UX Direction

## Design direction

The visual direction is:

**Corporate Editorial Engineering**

The interface should combine:

- modern minimalism;
- professional engineering software;
- editorial sophistication;
- institutional authority;
- precision;
- strong information hierarchy.

The atmosphere may draw inspiration from classic corporate environments and
the restrained visual sophistication associated with Succession, but must not
copy the series or sacrifice usability for decoration.

The product should feel premium, precise, calm, and trustworthy.

## Avoid

Do not use:

- generic SaaS dashboard aesthetics;
- excessive cards;
- large decorative gradients;
- glassmorphism;
- excessive shadows;
- excessive border radius;
- saturated colors;
- emojis as UI icons;
- decorative animations;
- gold as a dominant color;
- serif fonts in dense operational interfaces;
- unnecessary visual clutter.

## Visual principles

Prefer:

- generous negative space;
- strong typography hierarchy;
- thin borders and dividers;
- continuous surfaces;
- restrained use of color;
- highly readable tables;
- explicit interaction states;
- precise alignment;
- tabular numbers for monetary values when available.

## Typography

### Primary interface font

Geist.

Use for:

- navigation;
- tables;
- forms;
- buttons;
- labels;
- monetary values;
- operational interfaces.

### Editorial font

Instrument Serif.

Use sparingly for:

- login;
- home hero;
- empty states;
- selected large editorial headings.

Never use the serif font for:

- tables;
- dense forms;
- buttons;
- small labels;
- operational data.

## Icons

Use Lucide React exclusively.

Do not mix icon libraries.

Do not use emojis as interface icons.

## Radius

Use restrained border radius:

- small controls: 4px to 6px;
- cards and dialogs: maximum 8px;
- pills only when semantically appropriate.

Avoid making every element rounded.

## Shadows

Use shadows minimally.

Prefer borders and surface contrast.

Dialogs, popovers, and floating elements may use subtle shadows when elevation
needs to be communicated.

## Light theme

Core tokens:

- background: `#F5F5F1`
- surface: `#FFFFFF`
- sidebar: `#102E32`
- text-primary: `#171A19`
- text-secondary: `#69716E`
- primary: `#174A50`
- accent: `#A9864B`
- border: `#DFE1DC`

The light theme should use warm off-white surfaces with a deep petroleum-blue
sidebar.

## Dark theme

Core tokens:

- background: `#0C0F0F`
- surface: `#131817`
- sidebar: `#080B0B`
- text-primary: `#F3F2EC`
- text-secondary: `#969E9A`
- primary: `#39777C`
- accent: `#C1A05F`
- border: `#29302E`

The dark theme should feel deep, elegant, and highly legible.

Avoid generic medium-gray dashboard surfaces.

## Gold accent

Gold communicates emphasis and brand character.

Use it sparingly for:

- selected brand details;
- subtle highlights;
- small premium accents.

Do not use gold as the default primary button color.

## Theme behavior

Support:

- light;
- dark;
- system preference.

Persist explicit user preference locally.

No component should hardcode theme-dependent colors.

Use semantic design tokens.

## Layout

Initial target: desktop only.

No mobile or tablet implementation is required in the first prototype.

The main authenticated application uses:

- persistent left sidebar;
- primary content workspace;
- optional contextual headers;
- generous but efficient content spacing.

## Sidebar

Primary navigation:

- Início
- Orçamentos
- Composições, when implemented
- Base de preços
- Configurações

The bottom area may contain mock user information.

The sidebar should be visually authoritative but restrained.

## Interaction patterns

### Popover

Use for quick contextual actions:

- renaming;
- small settings;
- compact editing.

### Dialog

Use for short focused workflows:

- creating an estimate;
- confirmations;
- destructive actions.

### Searchable command dialog or contextual selector

Use for searching and selecting compositions.

The composition selector should support:

- search by code;
- search by description;
- clear display of unit;
- clear display of current unit price;
- keyboard navigation where supported.

## Tables

Tables are a central interface element.

Prioritize:

- readability;
- precise alignment;
- restrained row density;
- visible hover state;
- right alignment for numeric values;
- tabular monetary values;
- direct quantity editing where appropriate.

Avoid wrapping important codes or monetary values unnecessarily.

## Empty states

Empty states should be useful and restrained.

They should:

- explain what is missing;
- provide one clear next action;
- avoid excessive illustration or decoration.

## Motion

Use subtle motion only when it clarifies:

- state changes;
- dialog appearance;
- collapsible sections;
- hover and focus feedback.

Avoid decorative motion.