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

**Tres variantes más, del 10-ago** (siete apariciones en un día, así que no es anécdota):
- **Falta el permiso de paso, no el llamante**: un formulario público entero —tablas, antibot,
  consentimiento— cuyo `/f/<slug>` no estaba en las rutas públicas del middleware. El único usuario
  para el que existe (alguien sin cuenta) recibía un 307 a login.
- **Un gate escrito, probado y que no corre**: ver [[un-gate-que-cruza-dos-listas-es-ciego-a-lo-que-no-esta-en-ninguna]].
- **Una tabla de rastro sin un solo escritor**: `auth_events` con 0 filas y la pantalla diciendo la
  verdad sobre la tabla, que era falsa sobre el mundo.

Señal de alarma para buscarlo: un módulo con tests exhaustivos y **cero consumidores reales**. Y una
segunda, más barata: preguntarle a la BASE cuántas filas tiene la tabla que ese módulo escribe.
Ver [[el-control-que-deja-dentro-el-test-del-cambio-se-mide-a-si-mismo]]
