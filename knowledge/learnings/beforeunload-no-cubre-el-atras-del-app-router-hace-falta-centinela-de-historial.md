---
title: beforeunload no cubre el atrás del App Router, hace falta un centinela de historial
date: 2026-07-31
source: claude-code-session
tags: [nextjs, react, ux, formularios]
---
`beforeunload` solo cubre las salidas del **documento**: cerrar pestaña, F5, escribir otra URL. Con
el botón atrás de una SPA de Next no se dispara, porque el App Router cambia de ruta sin descargar
nada. Y ese es justo el caso que pierde el formulario a medias.

Next 16 no ofrece API para bloquearlo: lo único documentado es `onNavigate` de `<Link>`, que
intercepta clics en enlaces, no `popstate`. El patrón que funciona es un **centinela de historial**:
mientras haya cambios pendientes, `pushState` de una entrada extra con la MISMA url; el primer atrás
la consume sin navegar y da margen a preguntar. Si confirma, `history.back()` de verdad; si no, se
repone. Conserva el `history.state` actual al empujar, que ahí guarda el App Router su árbol de ruta.

Dos avisos honestos:
- **La entrada extra se queda en el historial** y no hay forma de retirarla sin navegar.
- **No cubre los enlaces internos** del layout (barra lateral, logo): para eso hace falta el patrón
  `NavigationBlockerProvider` + `CustomLink`, que toca toda la navegación de la app.

Lo delicado no es el guard, es el `isDirty`: si se pone a `true` al montar, el diálogo sale en cada
salida y molesta más que el bug. Exige dos condiciones (hay contenido real Y difiere del snapshot
inicial) y deja fuera lo que escriben los automatismos. Caso real: FacturaIA `/generar`, `qa-015`.
