---
title: n8n execute workflow devuelve el nodo terminal equivocado si hay 2+ ramas que se ejecutan a la vez
date: 2026-08-13
source: claude-code-session
tags: [n8n, execute-workflow, sub-workflow]
---
Al llamar a un sub-workflow vía `Execute Workflow`, si ese sub-workflow tiene **2 o más nodos sin
salida (terminales) que se ejecutan EN LA MISMA corrida**, el nodo llamador puede devolver el
output del terminal equivocado (ej. un nodo recién añadido con 0 items) en vez del terminal real
con los datos correctos. Sin error visible — el caller recibe `{}` o datos vacíos, silencioso.

**No es un problema si los terminales son mutuamente excluyentes** (ramas de un IF donde solo una
se dispara por ejecución) — eso ya es normal y seguro.

**Fix**: cualquier nodo/rama nueva que se añada a un sub-workflow debe converger en el ÚNICO
terminal real antes de que termine la ejecución — nunca dejarla colgando como salida propia,
aunque "no vaya a afectar la respuesta". Si la rama nueva puede legítimamente no tener nada que
hacer, que devuelva SIEMPRE 1 item con un flag (`shouldX: false`), nunca `[]` — 0 items corta el
flujo ahí mismo (ver [[n8n-worker-valida-todos-los-nodos-aunque-no-esten-en-el-path]] para el caso
simétrico) y el nodo de destino final nunca se ejecuta.

Caso real: Simarro, `Buscar_viviendas_catalogo` — 2 intentos rotos antes de la versión correcta.
