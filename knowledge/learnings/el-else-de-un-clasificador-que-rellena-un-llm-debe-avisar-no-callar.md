---
title: el else de un clasificador que rellena un llm debe avisar, no callar
date: 2026-08-10
source: claude-code-session
tags: [n8n, llm, notificaciones, anti-patron, elphis]
---
`Decidir etapa` (Elphis, `registrar-lead`) mapeaba `tipo_consulta` → etapa + `destino` de aviso:
`ingreso`/urgencia alta → ingreso; `familiar|paciente_actual|handoff` → recepción;
`callback`/fuera horario → recepción; **`else` → `destino='none'`**, y `should_notify` exige
`destino !== 'none'`. Como `tipo` es `(i.tipo_consulta || 'info')`, en ese `else` caían el
default Y **cualquier valor que el LLM inventara**: 65 de 73 ejecuciones en 14 días no avisaron
a nadie. Quedaban en el CRM, así que ningún error, ninguna ejecución roja.

Al medir el impacto, **cuenta entidades, no ejecuciones**: esas 73 ejecuciones eran 13 personas
(el workflow se llama ~10 veces por conversación y el dedup agrupa por teléfono+hora), así que
«30 avisos en el peor día» era en realidad 4. Con un pipeline reentrante, contar ejecuciones
infla el volumen y asusta al cliente con un número inventado.

El campo lo rellena un LLM vía tool, o sea que el conjunto de valores **no está cerrado** aunque
el `switch` lo trate como si lo estuviera. Un `else` que silencia convierte cada alucinación de
enum en un aviso perdido.

**Regla:** si un side-effect (aviso, escalado, alerta) cuelga de un enum que rellena un LLM, el
sumidero es el camino que AVISA — lo no clasificado se escala, no se calla. Ahí el fail-safe es
ruido de más, no silencio. Y al medir, cuenta nodos ejecutados, no ejecuciones en `success`.

Ver [[idempotencia-de-entidad-no-debe-gatear-notificacion-side-effect]] (mismo pipeline, la otra
vía por la que estos avisos ya se habían caído) · [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]] · [[env-fecha-mal-formada-fail-closed-no-fail-open]]
