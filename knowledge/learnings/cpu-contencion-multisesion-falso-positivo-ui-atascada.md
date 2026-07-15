---
title: contención de CPU entre sesiones paralelas puede parecer un bug de UI (skeleton/carga atascada)
date: 2026-07-15
source: claude-code-session
tags: [qa, cpu, multi-agente, worktree, debugging]
---

Con varias sesiones/worktrees Claude Code corriendo `next build`/`next dev` en
paralelo en la misma máquina (load average >10 en una máquina de 10 cores), una
vista que hace fetch real (200 OK verificado por red) puede quedarse VISUALMENTE
en skeleton/loading varios segundos — no por un bug de estado/acumulador, sino
porque el hilo principal de React/Fast Refresh está bloqueado compitiendo por CPU.
Diagnostiqué esto como "bug real" y delegué un fix antes de comprobar `uptime`;
un agente con la máquina descargada (load 4-8) no pudo reproducirlo ni una vez
tras esperas de 60s.

Antes de diagnosticar un "atasco" de UI como bug de código:
1. `uptime` + `ps aux | grep "next build"` — si hay contención real, es la primera
   sospechosa.
2. Esperar bastante más de lo intuitivo (30-60s, no 5s) antes de concluir "atascado".
3. Si hace falta delegar la investigación, pedir explícitamente reproducción con
   `uptime`/`ps aux` ANTES de tocar código, y que reporte "no reproducido" en vez de
   forzar un fix a código que no está roto.

Ver [[facturaia]].
