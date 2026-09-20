---
title: un cierre documental escrito antes del merge entra en main mintiendo
date: 2026-09-21
source: agh-iberica
tags: [git, documentacion, proceso, merge]
---
La PR de cierre describe el estado **en el momento de escribirla**: «#1937 OPEN, verde, sin
mergear». Si se mergea primero la de código, esa frase entra en `main` **siendo falsa** — y no la
detecta ningún gate, porque es prosa. Pasa siempre que el cierre se escribe antes que el merge, que
es el orden natural.

El arreglo NO es retocar la nota de sesión (es write-once: dice lo que era verdad al escribirse):

1. Rebasar la rama de cierre sobre la punta ya con el código dentro.
2. **Addendum fechado al final de la nota** — «escrito DESPUÉS del merge» — que retira los puntos de
   «qué queda vivo» que caducaron. El cuerpo, intacto.
3. **Snapshot reconciliado**: ése sí se edita, es un snapshot, no un log.
4. ⚠️ El rebase **caduca la línea del gate**: re-medir y SUSTITUIRLA antes del merge.

Detectarlo es barato: antes de mergear el cierre, `grep -nE "OPEN|sin mergear|esperando"` sobre su
diff. Ver [[un-snapshot-que-nombra-su-propia-punta-no-puede-acertar]].
