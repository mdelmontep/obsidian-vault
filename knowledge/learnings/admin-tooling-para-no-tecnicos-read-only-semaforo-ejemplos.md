---
title: admin tooling para owner no-técnico — read-only + semáforo + ejemplos
date: 2026-05-11
source: claude-code-session
tags: [admin-ui, ux, observability]
---

Panel admin que va a usar un dueño no-ingeniero (no devops, no SRE) debe seguir 4 reglas para ser útil sin ser peligroso:

1. **Read-only por defecto**: nada de "Run Now" / "Force Sync" / "Drop cache" / botones destructivos. Un usuario sin contexto los aprieta sin saber consecuencias.
2. **Semáforo verde / ámbar / rojo** como vista principal — escaneable en 2 segundos. El estado se calcula server-side, no se delega a interpretar números.
3. **Descripción en español** debajo del título técnico — qué hace ese módulo/cron/job en lenguaje de negocio.
4. **Ejemplo real concreto** (tooltip o modal) — "Pepe crea una factura, esto pasa, esto se actualiza". El owner entiende la utilidad sin leer código.
5. **Notif automática al fallar** en la campanita interna — el owner no abre el panel a diario, hay que avisarle.

**Caso real FacturaIA**: panel `/admin/system/crons` con esta receta. Mantenido deliberadamente sin "Run Now" pese a que técnicamente trivial — el riesgo de owner disparando manualmente un cron que muta BD supera el beneficio.

**Extensión**: si el panel acaba teniendo acciones (raras), envolverlas en confirmación + log + reversibilidad.
