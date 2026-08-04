---
title: recuperar en código un fallo del modelo sin contarlo es un tapón — la señal es parte del arreglo
date: 2026-08-04
source: claude-code-session
tags: [agentes, llm, telemetria, observabilidad, agh]
---
Caso AGH (#869): el modelo acertaba la intención y erraba la ENVOLTURA — emitía una LECTURA dentro del
array `writes`. El brain la devuelve a su sitio y el turno se contesta bien. Pero al recuperarlo
**desaparecía la señal que delataba el fallo** (`unknown_write_kind`): turno perfecto, defecto de
prompt invisible, y el error analysis semanal dejaba de poder decir si empeora.

Regla: **toda recuperación determinista de un fallo del modelo emite su propia señal.** Recuperar sin
contar convierte un defecto medible en uno que solo se nota cuando ya es grande.

Dos detalles que deciden si la señal sirve:
- **Kind PROPIO, no reciclar el del fallo.** Reutilizar `no_target_miss` («una capacidad que no
  tenemos») habría sido falso —la capacidad existe y se ejerció— y habría corrompido justo la métrica
  de cobertura que otro issue construyó. Precedente en el mismo repo: se cuenta también un camino que
  FUNCIONA (`verbatim_read`) cuando lo que hay que decidir es si aporta.
- **Comparar por identidad** (la función devuelve el MISMO objeto si no recupera nada) para que la
  señal no pueda emitirse de más.

Relacionado: [[campo-de-texto-libre-que-viaja-a-telemetria-es-un-canal-de-egress]] · [[agh-iberica]].
