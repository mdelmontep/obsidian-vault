---
title: colapso grid 0fr keyed al child — un child divergente queda visible e inert (parece menú muerto)
date: 2026-07-18
source: claude-code-session
tags: [css, frontend, sidebar, inert, a11y]
---

Patrón de colapso animado sin medir alturas: `.wrap { display:grid; grid-template-rows:1fr }`
+ `.wrap.collapsed { grid-template-rows:0fr }`, y el **hijo** con `min-height:0; overflow:hidden`
para que 0fr recorte de verdad. El `.wrap` NO tiene overflow propio.

Trampa: si un grupo anidado **reusa** `.wrap` pero envuelve su contenido en un hijo de clase
DISTINTA (caso real: `.nav-sublist` en vez de `.nav-list`), el selector `overflow/min-height`
no le aplica → el hijo se **desborda y queda VISIBLE aunque el grupo esté cerrado**. Y si ese
hijo lleva `inert={!open}`, los enlaces se ven pero **no se pueden clicar** → se presenta como
"el desplegable no funciona", no como glitch visual (regresión #993, fix #995 en FacturaIA).

Fix: extender el selector de colapso al hijo divergente (`.wrap > .nav-list, .wrap > .nav-sublist`)
y anular su margen vertical al cerrar (el margin queda fuera del overflow → residual). Regla:
un mecanismo de colapso keyed a una clase de hijo se rompe en silencio con cualquier hijo variante.
Verificar midiendo el alto del contenedor (ver [[playwright-boundingbox-mide-geometria-aunque-overflow-recorte]]).
Relacionado: [[css-clase-decorativa-compartida-trampas-cascada]] · [[nav-activo-por-startswith-enciende-el-ancestro]].
