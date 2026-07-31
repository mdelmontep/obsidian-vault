---
title: un tool que falla dentro de un ai agent de n8n deja la ejecución en success
date: 2026-07-31
source: claude-code-session
tags: [n8n, ai-agent, observabilidad, agentesia]
---

El AI Agent captura el error de sus tools y sigue conversando. La ejecución sale
**`success`** y el cliente recibe una confirmación de algo que no ocurrió.

Caso real (ChatBOT WhatsApp de Agentesia, `89B9QN23hOHDq6oP`): el `googleSheetsTool`
tenía `columns.mappingMode: defineBelow` con `columns.value = {}` → `NodeOperationError:
"At least one value has to be added under 'Values to Send'"` en **cada** lead. El bot
respondía "Listo, Alba, el equipo te llama". Ni una fila en la hoja. Solo se salvaba
porque el aviso de Slack sí salía.

- No auditar por `status` de la ejecución: leer `runData['<nodo tool>'][0].error`.
- Un tool con `defineBelow` y `value: {}` **nunca** ha funcionado — no es una regresión,
  es que nadie mapeó las columnas. Comparar contra el gemelo que sí funciona.
- Corolario de diseño: si el flujo promete algo al cliente, el fallo del tool debe cortar
  la confirmación, no tragarse.

Ver [[if-con-ambas-ramas-al-mismo-nodo-no-hace-nada]]
