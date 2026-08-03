---
title: una protección construida y no enchufada no la caza ningún test
date: 2026-08-03
source: claude-code-session
tags: [testing, gates, arquitectura, seguridad]
---
El límite de tasa estuvo **dos días** completo —seis dimensiones, sus tests, su gate— mientras la
composición tenía `rateLimit: async () => ({ allowed: true })`. API pública sin un solo límite, con 673
pruebas, lint, typecheck y build en verde.

**Ningún test puede cazarlo**, y ese es el punto: el doble que inyecta cualquier prueba ES un literal,
así que no hay forma de distinguir «doble legítimo» de «relleno olvidado» ejecutando código. Y el
fichero de composición no se ejercita sin la infraestructura real delante.

Fix: un gate ESTÁTICO sobre el fichero de composición — el hueco lo rellena un identificador asignado
desde una llamada a algo importado del módulo real, nunca una función escrita ahí mismo. Comprobar la
**procedencia**, no el nombre. Y si no encuentra ninguna composición, pararse en vez de aprobar.

Señal de alarma para buscarlo: un módulo con tests exhaustivos y **cero consumidores reales**.
Ver [[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]]
