---
title: controles de formulario nativos (select, date) no se pueden estilar — construir componente propio
date: 2026-06-18
source: claude-code-session
tags: [frontend, css, design-system]
---

El popup del `<input type="date">` y la **lista de opciones** de `<select>` los
pinta el SO/navegador en una capa fuera del CSS → imposible aplicar glass, marca
o cualquier estilo (solo el control cerrado es estilable, no el desplegable).

Para seguir un design system hay que **construir el componente propio**
(combobox/calendario), portado a `<body>` (ver
[[ancestro-con-backdrop-filter-anula-blur-descendiente-portar-popover]]).

Truco de adopción sin tocar 80 sitios: el **trigger reutiliza la `className` del
contexto** (`set-input`, `adm-select`, `filter-select`…) → conserva su identidad
visual; solo cambia la lista desplegable. `value` siempre string (castea
number/enum), `onChange` y efectos secundarios intactos.

Casos límite (optgroup, borde de error, autofocus por `ref`, uncontrolled): NO
dejarlos nativos — **ampliar el componente compartido** (props `group`/`invalid`/
`autoFocus`, o darle estado al uncontrolled). Una fuente única > excepciones.

Ya construidos en el repo (TuFacturaIA): `<DatePicker>` (`src/components/ui/date-picker.tsx`, ISO `YYYY-MM-DD`) y `<Select>` (`select.tsx`) → úsalos, NUNCA reintroduzcas `<input type="date">`/`<select>` nativos. Caso 2026-06-25: SEPA remesas "fecha de cargo" + mandatos "fecha firma" migrados de nativo a `<DatePicker>`.
