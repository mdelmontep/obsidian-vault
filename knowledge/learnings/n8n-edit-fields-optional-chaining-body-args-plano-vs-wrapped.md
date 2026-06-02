---
title: edit fields necesita optional chaining cuando el body llega plano (chat) vs envuelto en args (voz)
date: 2026-06-01
source: claude-code-session
tags: [n8n, expressions, gotcha]
---

Mismo webhook, dos clientes con shape distinto:
- Voz Retell manda el body envuelto: `body.args.X` (+ `body.call`).
- Tools de chat (`toolHttpRequest` con `specifyBody:keypair`) mandan el body PLANO: `body.X`.

Un `Edit Fields` con `$json.body.args.X` (sin `?.`) revienta con body plano porque `body.args` es `undefined` → `.X` lanza TypeError → n8n devuelve **null silencioso** y NUNCA llega al fallback `|| body.X`.

Fix: `$json.body?.args?.X || $json.body?.X || ''` en TODOS los workflows del tool, no solo el primero que arregles. Caso EcoBox: buscar/cancelar/mirar rotos (null → ventana GCal sin acotar, búsqueda con phone vacío) mientras reservar (ya migrado a `?.`) funcionaba. Ver [[n8n-langchain-toolcode-args-en-input-no-en-query]].
