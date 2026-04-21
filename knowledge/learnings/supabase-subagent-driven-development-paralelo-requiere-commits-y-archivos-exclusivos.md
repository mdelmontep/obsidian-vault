---
title: subagent-driven development paralelo requiere commits y archivos exclusivos
date: 2026-04-21
source: claude-code-session
tags: [claude-code, superpowers, workflow]
---

Al usar subagent-driven-development (skill de superpowers) con múltiples agentes en paralelo, tres reglas críticas:

1. **Commitear estado limpio ANTES de lanzar cada batch** — archivos uncommitted complican rollbacks y confunden al usuario si un subagente falla.

2. **Asignar archivos exclusivos por subagente** — si dos subagentes necesitan modificar el mismo archivo, secuenciarlos o asignar uno como "dueño". Conflictos de merge entre subagentes son difíciles de resolver.

3. **Si subagentes hit rate limit, continuar en main session** — no esperar al reset. Los subagentes devuelven "You've hit your limit" con 0 tokens. Implementar las tareas restantes directamente sin cambiar el flujo.

Probado con 24 tareas ejecutadas en bloques de 4-7 subagentes paralelos. Las tareas independientes (archivos distintos) se paralelizan bien. Las dependientes (ej: types → library → provider) deben ser secuenciales.

Organización efectiva por bloques:
- **Bloque A** (secuencial): migration SQL → types → libraries (admin, features, billing)
- **Bloque B** (paralelo 4): providers + feature gates (archivos independientes)
- **Bloque C-E** (paralelo 7): API routes + UI pages (cada subagente 1-2 archivos exclusivos)
