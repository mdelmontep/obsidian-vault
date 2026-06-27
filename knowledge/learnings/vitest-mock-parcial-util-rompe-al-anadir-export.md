---
title: vi.mock parcial de un módulo util rompe en silencio al añadir un export nuevo
date: 2026-06-27
source: claude-code-session
tags: [vitest, mocks, testing]
---

Un `vi.mock('@/lib/x/escape', () => ({ escapeHtml }))` parcial **reemplaza el módulo entero**. Cuando producción empieza a usar otro export del mismo módulo (`escapeAttr`), el mock no lo tiene → queda `undefined` → lanza al invocarlo.

Si la llamada está dentro de un `try/catch` (p.ej. un bucle por-org), el error se traga → el efecto downstream (`sendEmail`) nunca corre → el test falla con un `expect(...).toHaveBeenCalledOnce()` que dice "0 veces", **ocultando la causa real**.

Fix: mocks parciales de módulos util → `importOriginal` + spread, override solo lo necesario:
```ts
vi.mock('@/lib/x/escape', async io => ({ ...(await io()), escapeHtml: s => s }))
```
Así los exports que añadas después siguen siendo los reales y el mock no caduca.

Caso real facturaia 2026-06-27: 5 tests `stock-alarmas-email` rojos en main (el template `stock_alarma` empezó a usar `escapeAttr`); pasaron desapercibidos porque el CI estaba bloqueado por billing.

[[vitest-mock-admin-client-cuando-test-toca-wrapper-outbox]] · [[test-mocks-rename-import-path-no-rename-import]]
