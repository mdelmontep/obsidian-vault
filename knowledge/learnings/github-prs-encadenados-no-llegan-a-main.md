---
title: github prs encadenados no propagan a main al mergear
date: 2026-04-27
source: claude-code-session
tags: [git, github, workflow]
---

PRs encadenados (A→main, B→A, C→B): al mergear A en main, B y C se mergean en sus bases originales (A y B), no en main. Los commits de B y C NO llegan a main.

**Fix**: crear nuevos PRs desde cada rama directamente a main, o hacer merge local:

```bash
git merge origin/rama-encadenada
git push origin main
```

GitHub API tarda en calcular mergeabilidad tras crear el PR — si devuelve UNKNOWN, esperar o hacer el merge por git local.
