---
title: "literales BigInt (300000n) compilan en vitest/esbuild pero tsc <ES2020 los rechaza (TS2737)"
date: 2026-07-17
source: claude-code-session
tags: [typescript, vitest, testing]
---
Un test con `expect(x).toBe(300000n)` PASA en vitest (esbuild transpila a target moderno)
pero `npm run typecheck` (tsc con `target` < ES2020) lo rompe: "BigInt literals are not
available when targeting lower than ES2020" (TS2737). Verde en vitest ≠ verde en typecheck.
Fix: usa `BigInt(300000)` en vez del literal `n`. Frecuente en motores fiscales que comparan
céntimos como bigint. Relacionado: correr el typecheck con exit real
[[typecheck-pipe-tail-enmascara-exit]] (si no, este error pasa desapercibido).
