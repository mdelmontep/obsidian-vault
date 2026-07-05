---
title: import CSV de precios — desambiguar ES/US por presencia de coma, nunca asumir un locale
date: 2026-07-05
source: claude-code-session
tags: [csv, import, parsing, decimal, gotcha]
---

Un parser de precios de importación que hace `replace(/\./g,'')` incondicional (asumiendo SIEMPRE que el punto es separador de miles, convención ES) rompe con cualquier CSV en formato US/internacional: `"9.99"` se lee como `999` — inflación ×100, sin error ni aviso, porque `parseFloat` sigue devolviendo un número "válido".

**Fix**: desambiguar por presencia de coma antes de limpiar — si el string tiene `,`, es ES (puntos=miles, coma=decimal, `replace(/\./g,'').replace(',','.')`); si NO tiene coma, el punto ES el decimal y no se toca (formato US/JS, `parseFloat` directo). Mismo criterio que usa `parseNumeroEs` en TuFacturaIA (`src/lib/documents/precio-helpers.ts`) — si el proyecto ya tiene un helper así, reusarlo en vez de reimplementar el parseo en cada import/endpoint nuevo.

**Cómo detectarlo en review**: buscar `replace(/\./g` o `replace('.', '')` sin condicional previo sobre si hay coma en el string. Verificar con un caso de test explícito `"9.99"` → debe dar `9.99`, no `999`.

Caso real: TuFacturaIA, importador de catálogo/inventario (PR #766).
