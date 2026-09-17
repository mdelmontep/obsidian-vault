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

## Excepción medida el 16-sep-2026 (EcoBox): ese `|| body.X` envenena el campo `name`

El cuerpo de Retell tiene TRES claves —`args`, `call` y **`name`**— y ese `name` de primer nivel es
**el nombre de la tool**, no un dato del cliente ([[retell-custom-tools-comparten-webhook-y-se-rutar-por-body-name]]).
Con `args.name` vacío, `args?.name || body?.name` se queda con `"Reservar_cita"`: Google Calendar
publicó una cita titulada «Peritaje — Reservar_cita — 3254JBC — choque».

- La cadena de `||` solo es segura para claves que **no existan** en el primer nivel del emisor. Las
  que el proveedor usa como metadatos colisionan; en Retell, `name` y `call`.
- Fix: discriminar por la FORMA, no encadenar fallbacks entre formas.
  `(($json.body?.args ? $json.body.args.name : $json.body?.name) || '').toString().trim()`
- Corolario más caro: el `|| 'Cliente'` del final dejaba en **código muerto** la puerta
  `Validate input` que exigía `name notEmpty`. Un valor por defecto en la entrada desactiva la
  validación que exige ese campo, y la puerta luce en verde sin haber podido disparar nunca.

Ver [[normalizar-en-un-nodo-intermedio-no-protege-a-quien-relee-el-de-entrada]].
