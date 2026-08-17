---
title: vitest sale EXIT 1 por un unhandledRejection aunque 0 tests fallen (fuga de teardown pg)
date: 2026-07-07
updated: 2026-08-17
source: claude-code-session
tags: [vitest, testing, postgres, ci, flakiness]
---

Un run con **0 aserciones fallidas** puede salir **EXIT 1**: vitest marca el run como fallido ante
cualquier `unhandledRejection`. Una suite verde se ve roja y confunde el gate. Diagnóstico: buscar
"Unhandled Errors"/"originated in <fichero>", **no** el resumen (que dice 0 fail).

Caso real (agh-iberica): un `.pg` dropea su base efímera con una conexión `pg` abierta → el server la
termina → `57P01 terminating connection due to administrator command` sin handler.

🔴 **Corregido el 17-ago: `await pool.end()` antes del `DROP` NO basta.** Si el `DROP` lleva
`WITH (FORCE)` —que hay que llevarlo, o un vitest huérfano deja el DROP esperando para siempre— el
FORCE **mata las conexiones y puede ganarle la carrera al cierre del socket**: `pg` emite `'error'`
en el Pool igual. Medido: 10/10 escapan.

**Y el `pool.on("error", () => {})` por fichero es el arreglo que reincide** (tres veces en el mismo
repo: #275 → #792 → #1293): quien escribe el `.pg` número ocho no se acuerda. Lo que cierra la clase:

- **un punto único** que fabrique el pool con el manejador ya puesto, y
- que el manejador **DISCRIMINE** — traga `57P01` (y `ECONNRESET`/`EPIPE` sólo si el pool se está
  cerrando) y **relanza cualquier otro error**: un `() => {}` compra silencio, no salud, y se tragaría
  un fallo de conexión legítimo dentro de un test, y
- **un barrido** que se ponga rojo si alguien abre una conexión a la base efímera sin pasar por él.

Variante "CUELGA" (no rojo): tras matar runs, los hijos quedan zombis compitiendo por handles → el
siguiente run se cuelga. Fix: matarlos (`ps | grep vitest`) y re-correr. Distinto de
[[vitest-fileparallelism-false-tests-integracion-bd-compartida]] (colisión entre ficheros que
comparten BD): aquí es fuga de teardown de una BD efímera.
