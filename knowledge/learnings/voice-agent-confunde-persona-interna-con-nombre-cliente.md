---
title: voice agent confunde persona interna con nombre del cliente al transferir
date: 2026-05-25
source: claude-code-session
tags: [voice, retell, prompt-engineering, transferencia]
---

Cuando el voice agent tiene una lista de personas internas a las que derivar (ej. Silvia/Dani/Carlos) y el cliente dice "quería hablar con Dani", el LLM extrae "Dani" como `nombre_cliente` y luego se despide "Perfecto Dani, queda registrado".

Causa: el campo `nombre_cliente` solo dice "Nombre y apellidos del cliente". El LLM ve un nombre en la conversación y lo asigna sin distinguir rol.

Fix combinado:
- En `parameter.description` de `nombre_cliente`: "Nombre del cliente que LLAMA (NO Silvia/Dani/Carlos — esos son personal interno, jamás clientes)".
- En el prompt, variables explícitas: `PERSONA_SOLICITADA` vs `NOMBRE_CLIENTE`, con "NUNCA los confundas" + reglas separadas para cada uno.
- En la despedida, plantilla literal: "Perfecto [NOMBRE_CLIENTE], te llamará [PERSONA_SOLICITADA]".

Caso real Tecnocloud (Laura): aplicó tras llamadas falladas el 25/05. Universal a cualquier agente con derivación a personal interno conocido. Ver [[llm-tool-description-precondiciones-pesa-mas-que-prompt]].
