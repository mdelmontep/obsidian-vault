---
title: tool copiloto: campo en interface pero no en select → guard mudo
date: 2026-06-29
source: claude-code-session
tags: [copiloto, supabase, postgrest, debugging]
---

Campo presente en la interface TypeScript y en BD, pero ausente del `.select()` → llega `null` en JS.
Un guard `if (row.campo)` nunca dispara → preview pasa OK, execute falla en la RPC con error críptico.

**Caso real:** `ajustarStock.ts` — `gestiona_lotes` no estaba en el `.select()` de `resolveProducto`.
La RPC de mig 312 bloqueaba con `P0001` al ejecutar, pese a que el preview decía OK.

**Fix:** añadir el campo al `.select()` y al interface. Siempre que añadas un guard sobre un
campo de BD en una tool existente, verifica que ese campo esté en el `.select()`.

**Señal de alerta:** preview PASS + execute FAIL con error de RPC → campo faltante en select.
