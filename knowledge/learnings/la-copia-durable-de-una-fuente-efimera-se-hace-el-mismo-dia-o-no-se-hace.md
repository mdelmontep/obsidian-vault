---
title: la copia durable de una fuente efímera se hace el mismo día o no se hace
date: 2026-07-29
source: claude-code-session
tags: [documentacion, proceso, obsidian]
---

Tres veces el mismo fallo en el mismo proyecto (modelo WAPI del módulo Obras):

1. Los **2 vídeos con la narración de Natalia** (17-jul) llegaron por WhatsApp. Se transcribieron
   a `docs/architecture/obras/modelo-wapi-y-precios.md` el mismo día. **Esa copia sobrevive.**
2. El **manual completo transcrito** vivía en `~/Downloads/WAPI_MANUAL_COMPLETO.md` y el plan de
   Obras-IA lo cita como fuente. **Ya no existe.** `~/Downloads` no es un destino, es un buzón
   (y encima está TCC-bloqueado para Bash en este Mac).
3. El **PDF del manual** (29-jul) llegó por WhatsApp a
   `~/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/<uuid>/`. La caché de imágenes
   del propio Claude Code que llevaba la captura del usuario **se borró durante la sesión**.

Regla: material que llega por WhatsApp/Slack/Downloads y sustenta una decisión → **copia al repo
o al vault en la misma sesión**, antes de razonar sobre él. Y si el plan de otra sesión apunta a
una ruta de `~/Downloads`, dar por perdido el contenido y verificar (`ls`) antes de planificar
sobre él.
