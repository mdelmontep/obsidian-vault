---
title: empate de especificidad entre globals.css y un .module.css lo decide el orden de inyección, no tú
date: 2026-08-09
source: claude-code-session
tags: [css, css-modules, especificidad, refactor, facturaia]
---

Sacar CSS de un `<style jsx>` a un `.module.css` conserva la especificidad, pero **cambia
quién es el rival**. Si una regla global apunta al MISMO selector con la MISMA
especificidad, ya no gana "el que se inyecta después en runtime" (que era el `<style jsx>`,
siempre): gana el orden en que el bundler concatena los chunks, que nadie controla y que un
reordenado futuro invierte **sin error, sin lint y sin test**.

Caso real (auditoria-section, PR #1576): `globals.css:7512` tenía
`.set-table.audit td { padding: 10px 16px }` y el componente `padding: 8px 14px`. Ambos
(0,2,1). Funcionaba por casualidad. Mismo empate con `.search-box` global (`padding: 8px 14px`)
y la clase local del componente sobre el MISMO elemento.

**Fix**: anclar las reglas del módulo a una clase hasheada del propio componente —
`.panel :global(.set-table.audit) td` sube a (0,3,1) y el empate desaparece. Cuesta un
prefijo por regla y convierte "gana por orden" en "gana por especificidad".

**Detección**: antes de migrar, `grep` del selector global (`.set-table`, `.search-box`) en
`globals.css`. Si aparece con la misma forma, hay empate. El que no aparece no tiene rival.
Confirmarlo comparando estilos COMPUTADOS antes/después →
[[baseline-de-estilos-computados-por-ruta-de-dom-para-migrar-css-sin-e2e]].

Primos: [[checkbox-overlay-migracion-especificidad-css]] (global CONTEXTUAL gana por MÁS
especificidad, no por empate) · [[css-clase-decorativa-compartida-trampas-cascada]].
