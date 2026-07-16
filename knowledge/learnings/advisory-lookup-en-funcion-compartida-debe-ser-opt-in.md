---
title: un aviso advisory añadido a una función compartida debe ser opt-in + try/catch, nunca incondicional
date: 2026-07-17
source: claude-code-session
tags: [arquitectura, testing, supabase, patron]
---

Añadí un lookup "puramente informativo" (RPC de fuzzy-match para avisar de nombre
parecido) al final de una función find-or-create compartida (`crearClienteRapido`),
sin flag y sin try/catch. Esa función la llaman tanto tools conversacionales del
copiloto como `createDocument()` (ruta CRÍTICA: emisión de factura) y un endpoint
de voz. lint/typecheck/build pasaron limpios — el bug lo atrapó el CI al correr la
suite de tests: 5 tests rotos (cross-talk con el mock del RPC de numeración de
facturas + `TypeError: admin.rpc is not a function` en un mock que no lo esperaba).

**Regla**: si un side-lookup no cambia el resultado principal (solo añade un campo
opcional para UX), debe:
1. Ser opt-in (`checkX?: boolean`, default `false`) — el caller crítico ni se entera.
2. Ir envuelto en `try/catch` — un fallo del advisory NUNCA debe poder tumbar la
   operación principal ya confirmada.
Verificar con la suite completa (`npm run test`/`vitest run`), no solo
lint+typecheck+build — ese trío no ejecuta el código, solo lo tipa/compila.
