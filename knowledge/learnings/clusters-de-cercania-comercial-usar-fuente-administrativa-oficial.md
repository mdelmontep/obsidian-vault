---
title: clústeres de "cercanía" comercial (pueblo X sugiere Y) deben basarse en fuente administrativa oficial, no en agrupación a mano
date: 2026-08-17
source: claude-code-session
tags: [n8n, geografia, real-estate, arquitectura]
---
Al construir una feature de "si no hay nada en A, sugiero B/C por estar cerca" (búsqueda
inmobiliaria, reserva multi-sede, etc.) sin coordenadas reales disponibles, una agrupación a mano
por intuición ("estos 4 pueblos están cerca") es frágil y no escala: fácil clasificar mal un caso
límite (un pueblo fronterizo entre dos zonas) y cuesta ampliar cobertura sin repetir el mismo
riesgo.

**Mejor**: usar la división administrativa oficial ya existente (comarcas, distritos, códigos
postales agrupados) como base, y solo partir los grupos oficiales que sean demasiado anchos para
"cercanía real de comprador" (ej. una comarca que mezcla puntas opuestas de una ciudad). Verificar
el recuento total contra la fuente antes de codificar (ej. 179/179 municipios) — un lookup a medias
falla en silencio para los casos no cubiertos.

Caso real: Simarro, clústeres de proximidad para venta inmobiliaria — la versión ad-hoc inicial
clasificó mal Villaviciosa de Odón (sierra en vez de área metropolitana); cruzar contra la fuente
oficial (comarcas de la Comunidad de Madrid) lo detectó y corrigió, y permitió ampliar de 2 pueblos
a los 179 municipios de la región sin repetir el error. Ver [[simarro-voz-fixes-claro-clusters-17-ago]].
