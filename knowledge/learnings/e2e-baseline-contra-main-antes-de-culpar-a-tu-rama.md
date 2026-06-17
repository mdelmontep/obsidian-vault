---
title: e2e local rojo — baselinea las mismas specs contra origin/main antes de atribuir a tu rama
date: 2026-06-17
source: claude-code-session
tags: [e2e, testing, playwright, workflow]
---

Antes de "corregir" fallos de E2E smoke en tu rama, corre las **mismas specs sobre `origin/main`**
(árbol limpio + `git checkout origin/main` en el mismo dir → `node_modules` compartido, sin reinstalar).
Si fallan idénticas → pre-existentes/ambientales, 0 regresiones tuyas, **no toques nada** (corregirlas
sería fuera de scope).

Caso 2026-06-17 FacturaIA PR #340: 11 fallos en la rama = 11 fallos idénticos en main (stock con
estado, módulos feature-gated, avatar, timing middleware). Ninguno tocaba el código cambiado.

Ojo extra FacturaIA: `.env.test` apunta `E2E_BASE_URL` a **prod** (`app.tufacturaia.com`); para testear
tu código local hay que override `E2E_BASE_URL=http://localhost:3000` + dev server propio. Correrlo
sin override testea prod, no tu rama.

Familia: [[smoke-prod-en-transaccion-rollback]] · [[smoke-insert-directo-no-ejerce-el-motor-real]].
