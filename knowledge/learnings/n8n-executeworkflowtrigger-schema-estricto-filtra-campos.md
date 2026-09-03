---
title: n8n executeWorkflowTrigger schema estricto filtra campos no declarados
date: 2026-05-22
source: claude-code-session
tags: [n8n, sub-workflow, schema]
---

`executeWorkflowTrigger` con `inputSource:"workflowInputs"` solo deja pasar los campos declarados en `workflowInputs.values`. Si añades un campo nuevo en el caller (ej. `dry_run`) y no lo declaras también en el schema del trigger del sub-workflow, n8n lo elimina silenciosamente — no aparece en `Recibir inputs`.

Síntoma: la flag no surte efecto, el sub-workflow ejecuta como si no la hubieras pasado. Sin error.

Fix: declarar todos los campos opcionales en el schema del trigger con su tipo (`{name:"dry_run", type:"boolean"}`). Hay que actualizar el schema en TODOS los sub-workflows downstream, no solo en el primero.

Caso real Elphis 2026-05-22: `dry_run` en cascada por `clientify-upsert-contact` → `clientify-create-deal` → `agenda-book-slot` → `book-and-notify`, los 4 schemas hubo que tocar.

Caso real Elphis 2026-09-03: el caller mandaba `update_only:true` y `Recibir inputs` de `registrar-lead` no lo declaraba; la primera prueba del constructor entró por la rama normal y mandó un WhatsApp y un email **reales** a la recepción del centro con datos ficticios. Un flag que gatea un side effect no se prueba ejecutando: primero se comprueba que sale del trigger (runData del nodo), y solo después se ejecuta; y toda prueba se cierra verificando que el nodo del side effect NO aparece en `runData`. → [[un-flag-de-dry-run-que-el-reenviador-ignora-convierte-el-smoke-en-produccion]]
