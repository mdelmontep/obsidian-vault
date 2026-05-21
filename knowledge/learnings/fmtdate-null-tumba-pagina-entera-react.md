---
title: formatter date/string sin guard null tumba página entera React
date: 2026-05-21
source: claude-code-session
tags: [react, nextjs, formatters, null-safety, defensive]
---

`fmtDate(s: string): string` con `s.includes('T')` crashea con `Cannot read properties of null (reading 'includes')` cuando recibe `null`. React error boundary genérico → Chrome muestra "This page couldn't load" SIN error visible al user, solo en DevTools Console.

Síntoma engañoso: build + lint + typecheck verdes (signature `string` no `string | null`). Bug latente hasta que llega dato legítimo con `null` (columna BD `vto` nullable, factura insertada via SQL sin pasar por form que la rellena).

Patrón defensivo OBLIGATORIO en formatters compartidos:
- Signature `string | null | undefined`.
- Guard temprano return `'—'` (o fallback contextual).
- Test específico: `expect(fmtDate(null)).toBe('—')`.

Caso real: PR #66 2026-05-21. R-SMOKE-001/002 insertadas via SQL sin `vto` → `/recibidas` blank en producción tras deploy.

Regla: cualquier formatter `lib/format.ts` con typing strict que asume not-null debe revisarse contra columnas BD nullable. TS strict no protege contra runtime null cuando el cast viene de Supabase `select('*')`.
