---
title: github app installation no incluye repos creados después de la instalación
date: 2026-06-22
source: claude-code-session
tags: [github, dokploy, deploy, gotcha]
---

Una GitHub App instalada con acceso "selected repositories" NO concede acceso
automáticamente a repos creados después. Aunque el repo esté en la misma org
donde se instaló la app, hay que añadirlo manualmente.

Caso 2026-06-22: Dokploy configurado para clonar `AgentesIA-MAdrid/NotCaido`.
Repo creado → deploy fallaba con "Repository not found" pese a que la app
veía otros repos de la misma org.

Fix: GitHub → Settings → Applications → Configure (la Dokploy app) →
Repository access → añadir el nuevo repo explícitamente. Después el deploy
clona sin problema.

Aplica a cualquier GitHub App con scope "selected repositories": Dokploy,
Vercel, Netlify, CI de terceros, etc.
