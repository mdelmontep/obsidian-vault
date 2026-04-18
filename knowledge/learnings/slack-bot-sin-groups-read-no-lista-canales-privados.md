---
title: slack bot sin groups:read no lista canales privados
date: 2026-04-18
source: claude-code-session
tags: [slack, api, permisos]
---

`conversations.list` con `types=public_channel,private_channel` falla con `missing_scope` (`needed: groups:read`) si el bot no tiene ese scope.

Workaround: listar solo `types=public_channel`. Si necesitas acceder a canales privados, añadir `groups:read` en api.slack.com/apps → OAuth & Permissions.

Scopes actuales del bot "Bot incidencias": `chat:write, channels:manage, channels:read, users:read, canvases:read, canvases:write, channels:join, emoji:read`.
