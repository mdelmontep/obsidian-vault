---
title: migrar CSS de una pantalla sin E2E — baseline de estilos computados por RUTA de DOM
date: 2026-08-09
source: claude-code-session
tags: [css, css-modules, playwright, refactor, testing, facturaia]
---

Renombrar N clases a CSS Modules falla **perdiendo un estilo sin error**: nada peta, el
screenshot casi no cambia y el diff visual a ojo no lo ve. La red que sí lo ve:

1. **Identidad por RUTA, no por clase.** La clase es justo lo que cambia. Indexar cada nodo
   por su camino de índices de elemento desde la raíz del componente (`0:div/1:div/0:table/…`)
   y guardar `getComputedStyle` (~55 props + `getBoundingClientRect`), incluido `::after`.
2. **Forzar los estados que no se ven con datos cargados** interceptando la API con
   `page.route`: skeleton (handler que nunca resuelve), vacío (`{rows:[],total:0}`) y error
   (500). En auditoria-section esos tres tenían 9 clases propias, tres COMPUESTAS
   (`.skelCell.wTime`) — el tipo de clase que más se pierde.
3. **Diff con ruido conocido declarado**: CSS Modules **hashea el nombre del `@keyframes`**
   (`audit-detail-in` → `module__hash__audit-detail-in`) y el `transform` de una animación EN
   CURSO se muestrea en otro instante. Filtra esos dos o el diff sale rojo por diseño.
4. **Cruce en LOS DOS sentidos** de clases definidas en el CSS contra `s.x` usadas en el TSX:
   usada-sin-definir da `className="undefined"` (no lanza); definida-sin-usar es regla muerta.

Medido: 8.105 nodos × 7 estados, 0 diferencias reales (PR #1576). El baseline "antes" se
recaptura con `git stash` de los dos ficheros y `git stash pop`.

Ver [[empate-de-especificidad-entre-globals-y-un-module-lo-decide-el-orden-de-inyeccion]] ·
[[nombre-de-clase-css-modules-como-string-global-es-selector-muerto-sin-error]].
