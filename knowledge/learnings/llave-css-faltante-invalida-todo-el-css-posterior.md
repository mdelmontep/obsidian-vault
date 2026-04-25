---
title: llave css faltante invalida todo el css posterior
date: 2026-04-26
source: claude-code-session
tags: [css, debugging, facturaia]
---

Una `}` faltante en una media query de `globals.css` hizo que ~1800 líneas de CSS (agentes, settings, integraciones, plantillas, plan-billing) quedaran dentro de `@media (max-width: 700px)`, invisibles en desktop.

## Síntoma

Estilos que "no se aplican" en bloque — múltiples componentes afectados, no uno solo. Los selectores existen en el archivo pero el navegador los ignora.

## Diagnóstico rápido

```bash
grep -c '{' src/app/globals.css && grep -c '}'  src/app/globals.css
```

Si no coinciden, localizar con script:

```python
with open('src/app/globals.css') as f:
    lines = f.readlines()
depth = 0
for i, line in enumerate(lines, 1):
    for ch in line:
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
    if depth > 1:
        print(f'UNCLOSED at line {i}, depth={depth}: {line.rstrip()[:80]}')
print(f'Final depth: {depth}')
```

## Causa típica

Al editar reglas dentro de una media query se borra la `}` de cierre sin darse cuenta. Todo el CSS posterior queda anidado dentro de esa media query.

## Fix

Añadir la `}` faltante. En este caso: línea 1741 de `globals.css`, cerrando `@media (max-width: 700px)` antes del bloque `/* ============ AGENTES IA ============ */`.
