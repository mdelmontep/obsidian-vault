---
title: scheduled triggers de anthropic no acceden a repos privados de github
date: 2026-04-18
source: claude-code-session
tags: [claude-code, github, triggers]
---
Los remote agents (scheduled triggers de Claude Code) corren en la nube de Anthropic y no heredan las credenciales de `gh` del usuario. Si el trigger necesita clonar un repo privado, falla con "git_repository source could not be found". Soluciones: hacer el repo público, o conectar GitHub en claude.ai/settings.

**Actualización 2026-04-25**: el acceso a repos privados se solucionó (conectando GitHub en claude.ai/settings). Pero las llamadas de red salientes (curl a Slack, fetch a APIs externas) probablemente están bloqueadas en el sandbox del trigger. Ver [[remote-triggers-claude-probablemente-bloquean-curl-en-sandbox]].
