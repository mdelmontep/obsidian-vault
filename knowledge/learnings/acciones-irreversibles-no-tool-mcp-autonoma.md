---
title: acciones irreversibles no deben ser tool mcp autónoma
date: 2026-06-18
source: claude-code-session
tags: [mcp, seguridad, prompt-injection]
---
Las anotaciones de tools MCP (`readOnlyHint`/`destructiveHint`) son **hints**, no garantías: el cliente puede ignorarlas, no son enforcement de seguridad. Para acciones irreversibles o financieras (emitir factura a AEAT, pagos), confiar en que el cliente "pida confirmación" es insuficiente — el chat es el canal manipulable (prompt injection vía PDF/web que el agente lee; casos reales con specs de pago embebidas en contenido).

Patrón correcto: el agente **prepara** (crea un borrador) y devuelve un **deep-link a la app**, donde un humano confirma con sesión real (permisos + UI). El gatillo irreversible vive donde hay un humano, no en una tool. Defense-in-depth: el token del agente ni siquiera debe poseer el scope de la acción irreversible.
