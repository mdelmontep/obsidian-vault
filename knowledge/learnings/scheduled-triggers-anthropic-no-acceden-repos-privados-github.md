---
title: scheduled triggers de anthropic no acceden a repos privados de github
date: 2026-04-18
source: claude-code-session
tags: [claude-code, github, triggers]
---
Los remote agents (scheduled triggers de Claude Code) corren en la nube de Anthropic y no heredan las credenciales de `gh` del usuario. Si el trigger necesita clonar un repo privado, falla con "git_repository source could not be found". Soluciones: hacer el repo público, o conectar GitHub en claude.ai/settings.
