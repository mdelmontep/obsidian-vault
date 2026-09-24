---
title: en un semáforo con dos clases, la exclusiva pasa hambre sin reserva
date: 2026-09-24
source: facturaia
tags: [concurrencia, gates, semaforo, fia-gate]
---
`fia-gate` tiene dos clases de trabajo:
- **`mem`**: va de una en una;
- **`cpu`**: puede haber varias a la vez.

Con carga alta solo quedan 2 plazas de suelo. Cada vez que una se liberaba, la cabeza de cada clase competía por el lock y ganaba la que llegara antes.

Medido el 23-sep: **37 admisiones `cpu` mientras una `mem` esperaba** sin ninguna `mem` corriendo. Hubo esperas `mem` de 82-94 min. El FIFO dentro de cada clase no lo arregla, porque el hambre es **entre** clases.

**Fix:** una `cpu` no toma la última plaza del suelo si hay una `mem` VIVA esperando (tique con latido y PID vivo) y ninguna corriendo.
- No hace pasar hambre a `cpu`: `mem` va de una en una.
- Comprobar la vida del tique es obligatorio. Un tique de un proceso muerto reservaría la plaza para siempre.

Test que discrimina: congelar la `mem` con SIGSTOP y soltar una plaza. El semáforo viejo da el orden `C M`; con la reserva sale `M C`.

Resultado: 99 `mem` con 0 adelantamientos y espera máxima de 16 min. Ver [[el-suelo-de-un-semaforo-explica-quien-entra-no-cuanto-tarda]].
