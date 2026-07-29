---
title: roving tabindex sin selección deja el grupo entero fuera del tabulador
date: 2026-07-29
source: claude-code-session
tags: [a11y, frontend, componentes, facturaia]
---

Un grupo con roving tabindex (`tabIndex={selected ? 0 : -1}`, patrón WAI-ARIA de tablist/radiogroup)
funciona mientras SIEMPRE haya una opción activa. Si el control admite "todavía sin elegir" y le
pasas un `value` que no casa con ninguna opción, **todas las opciones caen a -1**: por teclado no
hay forma de entrar, y las flechas tampoco valen porque necesitan el foco ya dentro. Si además ese
campo es obligatorio para enviar, el formulario entero queda cerrado para quien no usa ratón.

Fix: sin selección, la primera opción utilizable entra en el tabulador.
`tabIndex={selected || (sinSeleccion && opt.value === primeraUtil) ? 0 : -1}`.

Dos avisos que valen más que el fix:
- **Migrar `<button>` nativos a un primitivo compartido puede quitar accesibilidad que venía gratis.**
  Los botones a mano se tabulaban solos; el primitivo "correcto" no.
- Antes de tocar un primitivo, mira sus hermanos de carpeta: en `src/components/ui/` el
  `radio-card-group.tsx` ya tenía este caso resuelto **y comentado**, y `segmented.tsx` no. Un
  patrón resuelto en un fichero y no en su vecino es deuda esperando a que alguien la pise.

Ver [[mide-el-reparto-de-fallos-antes-de-arreglar-el-que-te-cuentan]]
