---
title: slack_create_canvas no liga el canvas a un canal, y no hay tool de pin
date: 2026-08-05
source: claude-code-session — coordinación de equipo de tucrmia
tags: [claude-code, slack, mcp, gotcha]
---

`mcp__plugin_slack_slack__slack_create_canvas` crea un documento Canvas standalone: no acepta
`channel_id`, así que no queda adjunto a ningún canal por sí solo. Para que aparezca como el
canvas del canal hay que compartir el link con `slack_send_message` (o que alguien lo adjunte
a mano desde la UI).

Y no existe ninguna tool MCP para fijar (`pins.add`) un mensaje o canvas en un canal — hay que
pedirle a alguien del equipo con permiso que lo fije desde el menú (⋯ → Fijar en el canal).

Al montar coordinación de equipo por Slack desde Claude Code: crear el canvas, enviar el link
en un mensaje al canal, y pedir explícitamente que alguien lo fije — no asumir que quedó
visible ni pinneado solo por haberlo creado.
