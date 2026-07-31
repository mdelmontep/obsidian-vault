---
title: añadir un parámetro a un handler usado como onClick mete el evento dentro
date: 2026-07-31
source: claude-code-session
tags: [react, typescript, gotcha, seguridad]
---
Patrón que casi entra en producción y no lo habría cazado ni el typecheck ni un test feliz:

```tsx
// antes
const aprobar = async () => { ... }
<Button onClick={aprobar} />

// después: se añade un parámetro para el reintento confirmado
const aprobar = async (confirmarDuplicado = false) => { ... }
<Button onClick={aprobar} />        // ⚠️ el MouseEvent entra como confirmarDuplicado
```

React pasa el evento como primer argumento. Un `MouseEvent` es **truthy**, así que el
parámetro con default `false` llega siempre `true`: **toda** aprobación habría confirmado
duplicados en silencio, que es exactamente lo que el guard existía para impedir.

TypeScript no lo ve porque `(e: MouseEvent) => void` es asignable a un handler cuyo primer
parámetro es opcional. No hay error, no hay aviso.

Reglas:
- Al añadir un parámetro a una función que ya se usa como handler, **grepea sus usos** y
  envuélvela: `onClick={() => aprobar()}`.
- Si el parámetro gobierna algo peligroso (confirmar, forzar, omitir un guard), no le pongas
  default: hazlo obligatorio y que el compilador liste los llamantes.
- Un test que fije "la llamada normal NO manda el flag" vale más que uno del camino feliz.

Caso real: FacturaIA, confirmación de factura duplicada.
