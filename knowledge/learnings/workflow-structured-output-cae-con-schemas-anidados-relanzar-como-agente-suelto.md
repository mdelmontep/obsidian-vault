---
title: workflow structuredoutput cae con schemas anidados — relanzar como agente suelto
date: 2026-08-19
source: facturaia
tags: [claude-code, workflow, harness, gates]
---
En Workflows multi-agente, `agent(..., {schema})` con schemas de objetos anidados + enums
(el FINDINGS_SCHEMA típico de un gate: findings[] con severity enum) falla a ratos con
«StructuredOutput retry cap (5) exceeded»: 3 de 8 agentes en un día, mismo schema, mismas
misiones — no correlaciona con el contenido sino con el harness.

Mitigación que funcionó el 100% de las veces: relanzar ESA dimensión como `Agent` suelto
(mismo prompt y modelo) pidiendo «devuelve como texto final EXACTAMENTE un JSON con este
shape» — sin la herramienta StructuredOutput de por medio — y parsear el texto.

Prevención al diseñar el gate: schemas más planos (menos anidamiento/enums), o directamente
JSON-por-texto en las dimensiones y schema solo en la síntesis. El workflow entero NO se
relanza (los agentes buenos están cacheados por resumeFromRunId); solo la dimensión caída.
El síntoma en el resultado: `dimensiones` con status `no-ejecutada` — no contarla como
revisada, reponerla siempre.
