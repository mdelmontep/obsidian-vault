---
title: refactor UI grande con Claude Code — subagentes paralelos particionados por archivo
date: 2026-07-14
source: claude-code-session
tags: [claude-code, agentes, ui, workflow]
---
Para una tanda grande de mejoras UI con subagentes en paralelo, la clave NO es partir por feature sino por **conjunto de archivos disjunto**: dos agentes que tocan el mismo archivo (p.ej. dos features en `facturas-view.tsx`) se pisan. Reparte de modo que cada agente sea dueño exclusivo de sus ficheros; lo que colisiona (búsqueda + migrar-modales sobre los mismos listados) va **secuencial**, no en paralelo.

- Cada prompt: ruta absoluta + scope + "qué NO tocar" + "no corras build/lint/commit, solo edita" (el gate lo pasas tú UNA vez sobre el conjunto).
- Revisa el diff de cada agente (pueden proponer cosas que rocen inviolables) y deja que OMITAN con criterio lo que no encaja (drawer que no es modal, panel arrastrable) en vez de forzar.
- **Antes/después para artifact**: captura el "después" (árbol actual) con Playwright + storageState E2E; luego `git stash` del lote → captura el "antes" → `git stash pop`. Mismos datos, solo cambia el código.
- Gate `lint+typecheck+build` por lote; commits lógicos separados. Ver [[buscador-listado-lupa-expandible-no-fila-propia]] · [[ocultar-columnas-tabla-por-css-no-desmontar]].
