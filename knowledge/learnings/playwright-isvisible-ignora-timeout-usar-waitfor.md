---
title: playwright locator.isVisible({timeout}) no espera — usa waitFor para skips condicionales
date: 2026-06-13
source: claude-code-session
tags: [playwright, e2e, testing]
---

`locator.isVisible({ timeout })` NO espera: devuelve el estado **inmediato** del
DOM y el `{timeout}` se ignora silenciosamente. En una SPA (hidratación React,
fetch async) el elemento aún no existe → devuelve `false`.

Síntoma traicionero: un patrón `const hay = await loc.isVisible().catch(()=>false); test.skip(!hay)`
**skipea el test sin fallar** — parece "sin datos" cuando en realidad el
elemento sí carga 200ms después. Pierdes cobertura sin enterarte.

Fix: para esperar de verdad usa
`await loc.waitFor({ state: 'visible', timeout }).then(()=>true).catch(()=>false)`
o `expect(loc).toBeVisible({ timeout })` (ambos auto-esperan). Reserva
`isVisible()` solo para checks instantáneos sobre algo ya presente.

Relacionado: [[playwright-domcontentloaded-no-espera-hidratacion-rsc]].
