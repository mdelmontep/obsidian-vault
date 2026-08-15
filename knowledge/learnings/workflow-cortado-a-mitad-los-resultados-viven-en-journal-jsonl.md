---
title: un Workflow cortado a mitad no pierde lo hecho — está en journal.jsonl
date: 2026-08-15
source: claude-code-session
tags: [claude-code, workflow, auditoria, harness]
---
Un `Workflow` que muere por límite de sesión (41 de 55 agentes) **no pierde el trabajo de los que sí
terminaron**: cada `agent()` completado deja su valor de retorno en `<transcriptDir>/journal.jsonl`,
una línea `{"type":"result",...}` por agente. El resumen que devuelve la herramienta puede venir
truncado o con `sintesis: null`, y aun así el journal está entero.

Orden correcto cuando pasa:
1. **Volcar el journal a disco del repo ANTES de arreglar nada.** Si los hallazgos sólo existen dentro
   de una cifra («97 hallazgos»), la siguiente sesión no puede cerrarlos ni refutarlos. Ver
   [[un-hallazgo-que-solo-existe-como-cifra-no-se-puede-cerrar]].
2. Mapear agente→fase leyendo el prompt en `agent-<id>.jsonl` (el journal sólo trae `agentId`).
3. Reanudar con `Workflow({scriptPath, resumeFromRunId})`: los `agent()` con `(prompt, opts)` idénticos
   salen de **caché** al instante y sólo corren los nuevos.

Corolario útil: **subir un parámetro del script y reanudar es barato**. Subir el tope de refutación de
22 a 33 relanzó 23 agentes, no 77 — los buscadores y los refutadores previos vinieron de caché. Así se
compra cobertura sin repetir el gasto.

Distinto de [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]], que es para el
tool `Agent` (ahí lo recuperable está en el working tree y se reanuda con `SendMessage`).
