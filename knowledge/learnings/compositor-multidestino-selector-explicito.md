---
title: hilo con varios públicos → un compositor con selector de destinatario explícito
date: 2026-06-18
source: claude-code-session
tags: [ux, frontend, facturaia, admin]
---

Cuando un mismo hilo mezcla mensajes a destinatarios distintos (cliente / equipo
interno / agente IA) repartidos en **cajas separadas con destino implícito**, el
operador acaba escribiendo en la equivocada.

Caso real FacturaIA 2026-06-18 (`/admin/feedback`): tres textareas dispersas
(Responder al usuario / Instrucciones para Claude / Notas). Una instrucción para
Claude ("adelante") se registró como mensaje al **cliente** (`internal=false`).

Fix: **un único compositor** con selector de destinatario explícito y con color,
el botón y el placeholder cambian con la elección, **default al más seguro**
(nota interna, no se escapa email), y cada mensaje del hilo lleva etiqueta de
destino ("solo equipo" / "enviado al cliente" / IA). Ver también
[[acciones-irreversibles-no-tool-mcp-autonoma]] (mostrar destino antes de actuar).
