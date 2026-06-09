---
title: CSS Module — kebab-case no convierte a camelCase en Turbopack
date: 2026-06-09
source: fix(admin) 9a55964
tags: [css-modules, nextjs, turbopack, gotcha]
---

Next.js / Turbopack **no convierte automáticamente** los nombres de clase kebab-case a camelCase.

Si el CSS define `.kpi-grid` y el TSX accede como `s.kpiGrid`, la clase resuelve `undefined` → el elemento no tiene estilos. El contenido se muestra pero sin layout (texto plano en lugar de grid/card). No hay error en consola, falla silenciosa.

**Patrón correcto**: usar camelCase directamente en el CSS Module:
```css
.kpiGrid { ... }    ✅
.kpi-grid { ... }   ✗ — s.kpiGrid → undefined
```

**Cómo detectar rápido**: `grep -E "^\.[a-z]+-[a-z]" *.module.css` — si devuelve algo y el TSX accede en camelCase, están rotos.

**Referencia**: la regla de conversión automática sí existe en webpack/css-loader clásico pero Turbopack (Next.js 13+) no la implementa igual. Ver [[ia-kpi-strip.module.css]] como ejemplo de módulo que siempre fue camelCase y nunca falló.

Caso real: 4 paneles ia-ops (copiloto/ocr/voice/crons) mostraban texto plano en lugar de KPI cards. Raíz: ~30 clases kebab-case por módulo.
