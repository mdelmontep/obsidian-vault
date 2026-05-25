---
title: form defaults — respetar f.default, no usar !!config[key]
date: 2026-05-11
source: claude-code-session
tags: [react, frontend, forms, gotcha]
---

Rendering form fields cuyo valor puede venir de `org_module_config` (puede estar vacío) + un `default` declarado en el schema:

**Mal**:
```ts
checked={!!config[f.key]}     // ignora default-true cuando config={}
value={config[f.key] || f.default}  // 0 cae al default (mal para números)
```

**Bien**:
```ts
const effective = config[f.key] !== undefined ? config[f.key] : f.default
checked={typeof effective === 'boolean' ? effective : false}
value={String(effective ?? '')}
```

Distingue `false`/`0` explícito de `undefined` (no guardado).

**Caso real TuFacturaIA**: `ModuloConfig` mostraba `auto_categorizar`, `auto_marcar_cobradas`, `incluir_recurrentes`, `guardar_historial` como "Desactivado" en la primera carga aunque su default fuera `true`. Causa: `!!config[key]` con `config={}` → `false`. Fix: fallback al `f.default` del schema.

Aplica a cualquier UI que reabra un form con valores parcialmente guardados (settings, módulos, perfiles, edición).
