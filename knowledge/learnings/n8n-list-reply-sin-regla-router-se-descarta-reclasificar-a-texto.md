---
title: n8n: un list_reply sin regla en el router de botones se descarta en silencio
date: 2026-06-16
source: claude-code-session
tags: [n8n, whatsapp, routing, interactive]
---
Receptor WhatsApp clasifica msg_type='interactive' → Procesar Botón → switch de
botones. Si la id de la fila (list_reply) NO matchea ninguna regla del switch y
el fallback va a un nodo sin salida útil, el mensaje muere SIN responder (no es
error: la ejecución sale "success"). Caso TuFacturaIA 2026-06-16: las
selecciones de desambiguación `crear_doc_mov:`/`crear_doc_cli:` (que debían
volver al AGENTE para re-emitir el intent) caían en el switch de botones, no
matcheaban y se descartaban → el bot no contestaba al elegir movimiento/cliente.
Patrón: las selecciones de lista destinadas a re-alimentar al agente NO son
botones; reclasifícalas ANTES (en el parser: msg_type='text', text_body=id) para
que fluyan por el pipeline de texto→agente. Solo las acciones inline (confirmar/
cancelar) van al switch de botones. Cuando "no responde", verifica el camino con
la ejecución real (includeData=true → lastNodeExecuted). Ver
[[whatsapp-interactive-list-limites-y-row-id-pattern]].
