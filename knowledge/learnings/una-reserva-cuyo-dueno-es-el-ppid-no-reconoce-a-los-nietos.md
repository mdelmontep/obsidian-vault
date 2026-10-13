---
title: una reserva cuyo dueño es el ppid no reconoce a los nietos del dueño
date: 2026-10-13
source: facturaia (~/.claude/gate/fia-gate, commit 8296e89 de claude-harness)
tags: [semaforo, fia-gate, concurrencia, gates]
---
- Patrón: un semáforo retiene la plaza entre etapas a nombre de `$PPID` (el wrapper). Una etapa que pide plaza desde DENTRO (nieto: `gate-permisos` → build de staging) tiene otro `$PPID`, ve la reserva de su propio gate como ajena y espera a que caduque.
- Coste medido: 91 de 130 builds esperaron 290-310 s (TTL 300) del 30-sep al 13-oct; en los 91 la reserva era del mismo gate. El evento decía «otro gate retiene la plaza», y eso tapó el autobloqueo.
- Tell: espera ≈ TTL exacto, repetida, sin ningún otro gate vivo. Cruzar quién soltó la última plaza con el cwd de quien espera.
- Fix: el dueño viaja por entorno (`FIA_GATE_RES_OWNER`) y se hereda solo si ese pid es un ANCESTRO vivo del que pide; si no, `$PPID` como antes. Bajar el TTL solo acorta el síntoma y reabre la carrera A-B-A-B.
- Test que debe fallar antes del cambio: etapa que pide plaza dentro de otra (38 s con TTL 30 → 8 s), y un intruso que copia pid y seq file sin descender del dueño, que tiene que quedarse fuera (quitando la comprobación de ancestro, entra).
- Relacionado: [[una-cola-fifo-por-etapa-sin-retener-la-plaza-reparte-en-round-robin]], [[en-un-semaforo-con-dos-clases-la-exclusiva-pasa-hambre-sin-reserva]].
