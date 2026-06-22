---
title: un pill/chip de estado no debe reemplazar un dato accionable en un formulario denso
date: 2026-06-22
source: claude-code-session
tags: [frontend, ux, design-system, accesibilidad]
---

Tentación recurrente: "mete el aviso en uno de nuestros pills" para que se vea
consistente con el listado. Suele ser peor en un formulario denso de data-entry.

Por qué NO (debate 3 lentes: design-system, UX, a11y):
- **Pierde el dato**: el pill muestra una etiqueta fija ("Caduca pronto"), no el
  dato accionable ("Caduca el 07/07"). En un selector el usuario decide CON la fecha.
- **Contraste**: el fondo tintado del chip baja el contraste del texto a 11px frente
  al texto suelto sobre fondo plano (token `--warn-fg`/`--danger-fg`).
- **Jerarquía**: un chip relleno compite con los errores que SÍ bloquean (validación);
  un aviso informativo no debe pesar igual.

Regla: consistencia de **lenguaje** (mismo token de color warn/danger) ≠ consistencia
de **componente**. "Listado" (el objeto ES el estado, se escanea) ≠ "selector dentro
de un form" (el estado es un atributo del campo que rellenas). Diferenciar severidad
por color del texto (warn vs danger), no metiendo un chip.
