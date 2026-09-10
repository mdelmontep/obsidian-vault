---
title: la ventana del navegador de inspección no reflowa aunque `resize_window` diga ok
date: 2026-09-10
source: agency-portal
tags: [claude-code, browser, qa, frontend]
---
`resize_window` de claude-in-chrome devolvió éxito dos veces (390×860 y 420×900) y
`innerWidth` siguió en 1512: `outerWidth` sí cambió, el layout no. Ninguna media
query se reevaluó, así que **el viewport móvil no se capturó** — y decirlo es la
única salida honesta; lo móvil hubo que revisarlo leyendo el CSS.

- Comprobar SIEMPRE `innerWidth` con `javascript_tool` tras redimensionar. El «ok»
  de la herramienta no es una medida.
- Las coordenadas de un screenshot **caducan al cambiar el tamaño de la ventana**.
  Reusarlas clica otra cosa; así se firmaron dos escrituras reales en producción
  ([[el-dev-server-local-con-env-de-prod-convierte-cada-clic-de-qa-en-escritura-real]]).
- Un F5 puede servir el render viejo del bfcache y hacer creer que el código no
  llegó al disco. `cmd+shift+r` antes de diagnosticar nada.
