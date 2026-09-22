---
title: trinquete de baseline (bloquea solo lo NUEVO) — patrón reusable para deuda que no se puede cerrar de golpe
date: 2026-07-22
source: claude-code-session
tags: [ci, gates, deuda-tecnica, facturaia]
---
Patrón ya usado 3 veces en TuFacturaIA (inline-styles, design-debt, y ahora
vulnerabilidades npm): cuando una categoría de deuda tiene hallazgos
preexistentes que NO se pueden (o no toca) arreglar todos de golpe —algunos
bloqueados upstream, otros necesitan QA aparte—, un gate que bloquea sobre
CUALQUIER hallazgo deja el repo permanentemente rojo. La solución es un
trinquete: baseline commiteado (JSON) de lo ya aceptado + motivo, el checker
solo falla si aparece algo NUEVO fuera del baseline.

Estructura común (ver `scripts/inline-style-ratchet.mjs` y
`scripts/audit-ratchet.mjs`):
- `--write` regenera el baseline desde el estado actual (con `PENDIENTE:` a
  rellenar a mano si el motivo no estaba ya documentado).
- El check normal compara contra el baseline; permite que baje (arreglado
  sin tocar el baseline) pero bloquea que suba o aparezca algo nuevo.
- Wireado en pre-commit, condicionado al tipo de archivo que dispara la
  categoría (staged `.css`/`.tsx` para inline-style, `package-lock.json`
  para audit).

Antes de confiar en un checker nuevo: probarlo con un caso que DEBERÍA
fallar (quitar una entrada del baseline a mano, confirmar exit 1) — no basta
con que corra sin errores. Regla homóloga a la disciplina de loops/checkers
en general (ver memoria del agente `feedback_loop_engineering_disciplina`).

🔁 **El modo de fallo del patrón: un trinquete que nadie consolida le cobra a quien pase después**
(23-sep, vault de Obsidian). El trinquete de contexto de arranque (`scripts/context-budget.mjs`) salió
rojo en mi cierre. Antes de condensar nada restauré `origin/main` **puro** y volví a medir: **+7,6 KB
ya estaban ahí con CERO cambios míos**; lo mío eran 1,4 KB. O sea que el **84 % del rojo era deuda de
otras sesiones que cerraron sin correr el trinquete**. Un baseline solo aprieta si se consolida en el
mismo cierre que produce el cambio.

- Deja al siguiente ante dos malos incentivos: **subir el baseline por inercia** (el trinquete deja de
  medir) o **condensar lo que no es suyo** para pasar (poda a ciegas de trabajo ajeno). Los dos
  rompen el patrón, y ninguno deja rastro de que se rompió.
- La sonda que separa lo tuyo de lo heredado: **mide sobre `origin/main` limpio antes de tocar nada**,
  y resta. Sin ese control no sabes si estás pagando tu factura o la de tres sesiones.
- Corolario para el trinquete de un repo COMPARTIDO por sesiones simultáneas: correrlo en el cierre no
  es opcional ni cortesía — es lo único que impide que la deuda se acumule en el que llegue con prisa.
  Y si BAJA, consolidar también: un baseline flojo deja de apretar igual que uno inflado.
