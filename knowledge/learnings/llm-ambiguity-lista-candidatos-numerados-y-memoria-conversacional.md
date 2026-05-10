---
title: llm ambiguity con voz — lista candidatos numerados + memoria conversacional
date: 2026-05-10
source: claude-code-session
tags: [llm, voice, whisper, ux, n8n]
---

Cuando un LLM con tools (n8n AI Agent) busca un recurso por nombre y el usuario dictó por voz:

**Antipattern**: devolver `error: 'ambiguo'` con mensaje "dime el número exacto" o `error: 'no_encontrado'` con "dame el cliente". El usuario rara vez sabe el número, y si dijo el cliente mal por Whisper, repetir la pregunta es bucle.

**Pattern correcto**:
1. Instruir matching permisivo explícito (acentos, diminutivos, typos Whisper). "manuel" matchea "manvel"/"manuvel"/"garcia".
2. Si >1 match con confianza similar → devolver lista numerada `1) NUM · cliente · total · fecha` (max 5).
3. Si 0 matches → listar los 5 últimos abiertos como fallback ("¿es alguno?").
4. Aprovechar memoria conversacional (`memoryPostgresChat` en n8n): cuando el usuario responde "1" en el siguiente turno, el LLM recuerda los candidatos y resuelve a 1 match.

Esto convierte un dead-end en un flujo conversacional natural sin necesidad de mantener estado externo en el workflow.
