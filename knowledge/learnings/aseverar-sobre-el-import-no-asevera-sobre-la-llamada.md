---
title: un candado que asevera el import no asevera la llamada
date: 2026-08-17
source: claude-code-session
tags: [testing, mutacion, seguridad, metodo]
---
Un contrato de la API v1 aseguraba que `POST /v1/webhooks/{id}/test` reutiliza `deliverOne` —la entrega
con protección anti-SSRF— en vez de hacer su propio `fetch`, con
`expect(src).toContain("import { deliverOne")`. **Sustituir la llamada por otra función deja los 6 tests
en verde**: el import sobrevive al cambio. No lo vio la revisión; lo cazó el barrido de mutación
(`~/.claude/bin/mutate`). Fix: aseverar el **uso**, `expect(src).toMatch(/\bawait\s+deliverOne\(/)`.

Regla al escribir cualquier candado sobre el fuente: la declaración y el import son **inventario**, la
llamada es la **conducta**. Si se puede satisfacer sin que se ejecute lo que vigila, no es un candado.
Ver [[un-export-cuyo-unico-importador-es-su-test-sale-verde-en-todo]] ·
[[una-proteccion-construida-y-no-enchufada-no-la-caza-ningun-test]] ·
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
