---
title: n8n "success" no implica que la ejecución recorrió el camino crítico
date: 2026-06-30
source: claude-code-session
tags: [n8n, debug, regresion]
---

Al datar cuándo se rompió un workflow por webhook, filtrar por `status=success`
engaña: muchos "success" son ramas no-op (ej: webhooks de *status* de Meta/WhatsApp
—entregado/leído— que un `If` descarta sin tocar la lógica real).

El bug solo se dispara en el camino crítico, así que entre la edición que lo
introdujo y el primer fallo pueden pasar días de "success" no-op → falso
"funcionaba hasta ayer".

Fix: abrir las ejecuciones OK y confirmar que recorrieron el **nodo que ahora
falla** (mismo `_outcome`/path), no fiarse del status. Distinguir trigger real
vs eco/status antes de concluir "se rompió tal día".

Caso real: chatbot WA Elphis, ver [[incidents]] (2026-06-25).
