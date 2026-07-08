---
title: en HITL, una intención compuesta (alta implícita + acción) se colapsa con prerequisite injection, no con diálogo multi-turno
date: 2026-07-08
source: claude-code-session
tags: [agentic, hitl, agh-iberica, diseño]
---

"Añade a Juan Pérez como candidato a la oportunidad de Dragados" cuando Juan Pérez no existe:
la solución obvia es un diálogo — clarify "¿lo doy de alta?" → confirma → RETOMA la intención
original ("¿lo añado a la oportunidad?"). Esa retoma es el punto frágil: cualquier respuesta
ambigua del usuario en el turno intermedio ("añádele") no se entiende y el bucle se repite,
perdiendo la intención.

Mejor: en `prepare()` del write que referencia la entidad, si no existe, inyectar su alta como
**prerequisite del mismo batch** (mismo patrón que `crm.createClient` cuando `clientName` no
resuelve en `opportunity.create`). El usuario ve y confirma AMBOS de una vez ("dar de alta a
Juan Pérez; añadirlo como candidato..."); al confirmar se ejecutan en orden porque los writes de
un batch corren secuencialmente — el `execute()` del segundo write resuelve por nombre y
encuentra al recién creado. No hay turno intermedio, así que no hay dónde perder la intención.

Aplica a cualquier agente HITL con batches ordenados. Ver [[hitl-reresolver-nombre-id-en-execute-no-inyectar-en-prepare]] (matiz: inyecta VALORES derivados/prerequisites completos, no ids sueltos).
