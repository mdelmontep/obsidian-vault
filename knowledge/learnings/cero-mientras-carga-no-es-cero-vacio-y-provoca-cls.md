---
title: el cero de "aún no lo sé" no es el cero de "está vacío", y decide layout
date: 2026-07-27
source: claude-code-session
tags: [react, performance, cls, ux, facturaia]
---

`/ingesta` tenía el mayor salto de layout de la app (CLS 0,212) por una línea:

```ts
const slimDrop = totalCount > 0   // ❌ totalCount vale 0 mientras carga
```

Ese `0` no significa "bandeja vacía": significa **"todavía no lo sé"**. Con él se pintaba la zona de
arrastre grande (`min-height: 140px`) y colapsaba a ~54 px al llegar el conteo, subiendo **86 px** todo
lo de debajo. Fix: `bandejaLoading || totalCount > 0` → **0,212 → 0,058**.

Patrón: cualquier contador/lista que arranque en su valor neutro y decida **tamaño o presencia** de un
elemento va a provocar CLS. El estado de carga es un tercer valor, no un sinónimo del vacío. Y elige el
default por frecuencia: asumir "hay datos" acierta en toda org que use la pantalla a diario; el salto
queda solo para el primer uso.

Para atribuir el culpable, no basta el número agregado:
`PerformanceObserver({type:'layout-shift', buffered:true})`, filtrar `hadRecentInput` y volcar
`entry.sources[].node` con `previousRect`/`currentRect`. Eso señala el nodo que se mueve.

Ver [[cpu-contencion-multisesion-falso-positivo-ui-atascada]] ·
[[el-universo-comparable-es-lo-que-se-persiste-no-lo-que-se-carga]] · [[facturaia]]
