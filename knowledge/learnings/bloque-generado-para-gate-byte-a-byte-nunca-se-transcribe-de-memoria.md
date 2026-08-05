---
title: bloque generado que un gate compara byte a byte nunca se transcribe de memoria
date: 2026-08-05
source: claude-code-session
tags: [codegen, gates, migrations, postgres]
---

Cuando un gate compara "¿el bloque embebido en el fichero == la salida fresca del generador?"
(caso: `access:check`/G-ACCESS-DRIFT comparando el `crm_can()` SQL dentro de una migración contra
`node scripts/gen-access.ts`), escribir ese bloque de memoria al redactar la migración introduce
errores silenciosos: orden de ramas cambiado, un `coalesce()` que falta, bloques de política
enteros ausentes. El gate los caza, pero solo si se corre — y mientras tanto el fichero es
sintácticamente válido y "parece" correcto a ojo.

Fix: nunca teclear el bloque generado. Capturar el stdout exacto del generador en un script
de un solo uso y empalmarlo byte a byte (verificado con igualdad de string, no con lectura visual)
en el fichero destino. Aplica a cualquier patrón codegen+diff-gate: OpenAPI generado, tipos de BD,
políticas RLS, SDKs — la regla es la misma que para no transcribir un `openapi.json` a mano (ver
[[openapi-spec-mantenido-a-mano-deriva-del-handler]]), pero un nivel más estricto: ahí basta con que
el contrato *describa* el handler; aquí el gate exige igualdad literal.
