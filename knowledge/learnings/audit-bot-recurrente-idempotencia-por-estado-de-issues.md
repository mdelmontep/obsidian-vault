---
title: bot de auditoría recurrente — la idempotencia vive en el estado de los issues, no en la fuente de datos
date: 2026-07-13
source: claude-code-session
tags: [agentes, auditoria, idempotencia, observabilidad]
---
Un bot que corre cada semana leyendo trazas/telemetría (Langfuse, logs) y abre issues re-detecta lo MISMO cada semana salvo que deduplique bien. La fuente de datos NO sabe qué está "arreglado u obviado" — es solo datos. La verdad vive en el **estado de los issues de GitHub**, y el bot debe deducirla:

- Dedup contra issues ABIERTOS (no re-abrir un pendiente) **Y CERRADOS**. El fallo típico: dedup solo contra abiertos → un cerrado se re-abre desde trazas viejas aún en ventana, y los "esperado/wontfix" recurren cada semana.
- **Cómo "le dices" que algo está resuelto = cerrando su issue.** Cierre normal (corregido) → suprimir salvo REGRESIÓN real (trazas POSTERIORES al `closedAt`). Cierre con label `wontfix` (esperado/obviado) → **supresión permanente**.
- La ventana temporal ayuda (un fix desplegado deja de aparecer y sale de la ventana en N días → auto-limpieza), PERO una ventana que CRUZA el merge de un fix re-surface clases ya arregladas desde trazas pre-fix → el triage debe cruzar cada hallazgo contra lo mergeado, no fiarse del bot.
- Maker (el bot) propone; checker (humano, o segunda pasada con contexto fresco) verifica antes de tratar un hallazgo como real: ~mitad suelen ser cubiertos/esperados/stale.

Ver [[maker-checker-re-auditar-fixes-propios-antes-de-merge]] · [[observabilidad-nueva-destapa-bugs-viejos-en-silencio]].
