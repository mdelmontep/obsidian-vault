---
title: pnpm/action-setup@v4 rompe si declaras versión en workflow Y en packageManager de package.json
date: 2026-05-07
source: claude-code-session
tags: [github-actions, pnpm, ci, gotcha]
---

`pnpm/action-setup@v4` lee la versión de pnpm de DOS sitios:

1. Su propio input `version: 10` en el workflow.
2. `packageManager: "pnpm@10.33.3"` de `package.json`.

Si ambos están definidos → falla con:
```
Error: Multiple versions of pnpm specified:
  - version 10 in the GitHub Action config with the key "version"
  - version pnpm@10.33.3 in the package.json with the key "packageManager"
```

CI rojo en TODOS los PRs de la rama afectada. Caso real: Dani añadió `packageManager` en commit aparte para anclar en Docker, sin tocar workflow. Main rojo + cualquier PR rojo.

Fix recomendado por pnpm (la opción más limpia y future-proof):

```yaml
- name: Setup pnpm
  uses: pnpm/action-setup@v4
  # sin `with: version: X` — lee de packageManager
```

Eliminar el `with: version: N` de TODOS los jobs del workflow. Ya estaba en `package.json`, action lo lee automáticamente. Beneficio extra: una sola fuente de verdad para la versión de pnpm.
