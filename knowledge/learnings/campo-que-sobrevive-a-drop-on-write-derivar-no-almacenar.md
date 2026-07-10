---
title: un dato que debe sobrevivir al drop-on-write se DERIVA de la fuente durable, no se almacena en el store que se limpia
date: 2026-07-10
source: claude-code-session
tags: [agentes-codigo, estado-conversacional, hitl, diseño, agh-iberica]
---
En una máquina conversacional, el contexto anafórico (ventana de turnos, entidades recientes) se LIMPIA en las fronteras write/confirm/cancel (drop-on-write): un ordinal/deíctico no debe resolver contra estado previo a un write intermedio. Pero algunos datos SÍ deben sobrevivir al write — p.ej. el "cliente activo": tras «apunta X»→confirmar, «¿y sus reuniones?» debe seguir resolviendo.

Trampa: si metes ese dato en el mismo ring que se dropea, caduca y regresas comportamiento. Y el eval unit-level (que inyecta el contexto directo al intérprete) NO lo detecta — el fallo solo aparece en el flujo across-write real.

Patrón: para lo que debe sobrevivir, NO lo almacenes en el store efímero; **derívalo cada turno** de una fuente que ya persiste por otra razón (aquí `lastClientId`, que se reconstruye en cada confirm/cancel). Se proyecta fundido en la misma lista que ve el LLM (fuente única de "entidad activa") sin heredar el TTL/drop del ring. Caso real: L2b de #118 AGH — subsumir `activeClientName` en `recentEntities` derivándolo, no almacenándolo. Añadir SIEMPRE un test determinista across-write (write→confirm→consulta) que el eval no cubre.
