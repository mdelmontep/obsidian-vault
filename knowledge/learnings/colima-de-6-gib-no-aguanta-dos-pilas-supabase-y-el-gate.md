---
title: la vm de colima de 6 gib no aguanta dos pilas de supabase y la integración del gate
date: 2026-10-13
source: facturaia (gate del PR #3473)
tags: [colima, supabase, gate, oom]
---
**Qué pasa:** con la pila `fia-dbtest` y otra pila Supabase (learn-agentesia) vivas en la misma VM de Colima de 6 GiB, la integración del gate la tumba por OOM. Contenedores muertos y, al reintentar, la base sale `SIN_CONFIGURAR`.
**El tell:** `docker ps` con contenedores `Exited (137)`, carga del Mac >40, y rojos de integración como `AuthRetryableFetchError: Processing this request timed out` o `Hook timed out` en `afterAll`, sin una aserción rota.
**Fix:**
- `supabase stop` + `supabase start -x …` en la pila compartida, avisando antes a quien la use.
- Repetir el gate con la carga por debajo de 15. Con otras sesiones en cola del semáforo, esperar su turno: no es un bug del PR.
**Fondo:** o se apaga la pila ajena mientras corre el gate o se sube la VM (`colima stop && colima start --memory 10`), que es decisión de Manuel.
