---
title: TuFacturaIA tiene 4 dialectos de input CSS — .field genérico fuera de su scope se ve sin diseño
date: 2026-07-17
source: claude-code-session
tags: [facturaia, css, design-system, frontend]
---

TuFacturaIA acumuló 4 sistemas de campo de formulario distintos, cada uno correcto solo en su contexto:

- `.field` global (`globals.css`) — card de fila editable en paneles de detalle (border+bg+padding propios).
- `.auth-card .field` — override que resetea `.field` a "solo label+input" para login/registro.
- `.ob-input` — estilo glass del wizard de onboarding.
- `.set-input` — subrayado de Ajustes.
- `ui/input.tsx` (`Input`) — componente "línea contable glassy" (2026-06-11), el correcto para modales nuevos.

Usar `className="field"` a pelo en un modal (fuera de `.auth-card`) hereda el CSS de "card de detalle" sin querer → se ve con caja pesada, "sin diseño" (caso real: `cambiar-telefono-modal.tsx`). Antes de poner un campo en un modal nuevo, usar `ui/input.tsx` — ya trae label/error/success/iconLeft/iconRight.

**Pendiente de arrastre**: mismo bug en `enroll-2fa-modal.tsx`, `cerrar-cuenta-modal.tsx`, `seguridad-section.tsx` — no tocados aún.
