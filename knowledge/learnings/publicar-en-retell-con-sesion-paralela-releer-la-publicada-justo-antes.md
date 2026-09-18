---
title: publicar en retell con otra sesión viva: releer la publicada más alta justo antes de escribir
date: 2026-09-18
source: elphis-psicologia
tags: [retell, agentes-voz, sesiones-paralelas, gotcha]
---
Elphis Psicología, 18-sep: comparé v19 con v20, y la sesión paralela publicó la v20 (rediseño, otras herramientas) **entre mi lectura y mi escritura**. Mi v21 salió de un prompt de mi rama y pisó el suyo: referenciaba herramientas que ya no existían. Restaurado en v22, idéntica a la v20 campo a campo.

- Una versión publicada no se parchea (400 «Cannot update published LLM»): `create-agent-version {base_version}` → `update-retell-llm?version=<response_engine.version>` → `update-agent?version=` → `publish-agent-version`.
- El script fija `EXPECTED_BASE` y **aborta** si la publicada más alta no es esa (`list-agent-versions` pagina: `has_more`/`pagination_key`).
- Parchea **solo el campo** que cambias, nunca el prompt entero desde tu rama: el prompt vivo puede ser de otra rama.

Ver [[copiar-la-config-de-un-agente-vivo-copia-una-version-que-sigue-moviendose]] · [[un-borrador-y-la-version-publicada-no-son-comparables-el-control-es-otro-borrador]]
