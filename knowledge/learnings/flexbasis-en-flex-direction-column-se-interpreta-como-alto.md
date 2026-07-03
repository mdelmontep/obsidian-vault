---
title: flex-basis pensado para ancho se interpreta como alto si el flex-direction pasa a column en mobile
date: 2026-07-03
source: claude-code-session
tags: [css, flexbox, mobile, frontend]
---

Un elemento con `flex: 1 1 240px` (pensado para dar ancho mínimo en una fila) se convierte en un bloque de **240px de ALTO** en cuanto el contenedor cambia a `flex-direction: column` en el media query mobile — `flex-basis` siempre mide a lo largo del eje principal, que rota con la dirección.

Síntoma: un input/buscador que se ve normal en desktop pero se infla a un bloque vacío gigante en mobile, sin ningún error visual obvio en el código que lo causa (el bug está en OTRO breakpoint, no donde parece).

Fix: en el media query que cambia a `column`, resetear explícitamente ese elemento — `flex: none; width: 100%;` — no basta con que el resto de reglas de la fila ya estén sobreescritas.

Caso real: TuFacturaIA, sección Auditoría (`auditoria-section.tsx`), buscador con `flex: 1 1 240px; min-width: 220px`.
