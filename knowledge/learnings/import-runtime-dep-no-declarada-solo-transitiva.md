---
title: import en runtime de un paquete no declarado en dependencies (solo transitivo/dev) = drift de versión + CVE silenciosa
date: 2026-06-19
source: claude-code-session
tags: [node, dependencias, supply-chain, seguridad, undici]
---
`import { Agent } from 'undici'` en código de producción, pero undici NO estaba en
`dependencies` — solo llegaba transitivamente vía `jsdom` (una devDependency). Next lo
bundlea desde esa copia (7.25, con CVE de bypass de validación TLS) sin control de
versión.

Doble riesgo: (1) la versión la fija un árbol ajeno y deriva sin que lo controles;
(2) la CVE de undici debilitaba justo el Agent anti-SSRF construido sobre él.

Detección: `npm ls <pkg> --omit=dev` vacío + un `import` de ese pkg en `src/` =
landmine. Regla: todo paquete importado en runtime debe estar en `dependencies`
explícitamente (no confiar en hoisting transitivo ni en una devDependency). Fix:
declararlo + `overrides` a versión parcheada. Caso TuFacturaIA dispatcher webhooks
(auditoría 2026-06-19). Ver [[ssrf-validar-dns-no-cierra-rebinding-sin-pinar-ip]].
