---
title: enum emitido por dos fuentes con vocabularios distintos → normalizar a canónico antes de switch/dedup
date: 2026-07-09
source: claude-code-session
tags: [arquitectura, enum, dedup, ui, gotcha, facturaia, fiscal]
---
Cuando el MISMO tipo/enum lo emiten dos generadores con vocabulario distinto
(p.ej. motor TS código `C-01` vs RPC SQL alias `borradores_en_periodo`) y no hay
tabla de equivalencia canónica, dos bugs SILENCIOSOS aparecen a la vez:
- **Switch/`.filter` por el string crudo** → la rama nunca matchea (el valor real
  nunca es el esperado) → todo cae al `default` sin error. Código muerto invisible.
- **Merge con dedup por string crudo** → `'C-02' !== 'verifactu_rechazada'` nunca
  colisiona → el mismo item sobrevive dos veces → el usuario ve duplicados.
Fix: un módulo source-of-truth con `tipoCanonico(x)` (colapsa alias→código) +
`label(x)` (nunca mostrar el código crudo al usuario, es jerga). Todo consumidor
—switch UI, `defaultBuildHref`, dedup del merge, display— normaliza con él.
Caso real TuFacturaIA PR #810: cuadres fiscales; `cuadre-meta.ts`. El drawer
resolvía 0 cuadres y C-02/03/04 salían duplicados en el panel.
Ver [[helper-validacion-canonico-front-back-evita-divergencia]] · [[cliente-react-bypasa-endpoint-canonico-bug-fiscal-latente]].
