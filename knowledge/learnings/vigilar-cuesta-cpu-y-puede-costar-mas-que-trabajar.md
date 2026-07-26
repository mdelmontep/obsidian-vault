---
title: vigilar cuesta cpu y puede costar más que el trabajo que vigila
date: 2026-07-26
source: claude-code-session
tags: [postgres, supabase, monitorizacion, performance, crons]
---

Al auditar `pg_stat_statements` buscando la consulta de usuario que satura la BD,
lo que sale arriba puede ser la propia maquinaria de observabilidad. Mirar cuesta.

Caso FacturaIA 2026-07-26 (la instancia acabó sin CPU y tumbó producción):

- `get_org_usage()` — **216.511 llamadas, 4.081 s, el mayor consumidor de la
  base**, por delante de cualquier consulta de negocio. Salía del
  `system-health-sweep`: 6 claves de cuota × ~25 orgs × cada 10 min = 2,8 s de
  `COUNT(*)` por barrido. Y las cuotas son contadores MENSUALES: una vez por hora
  sobra.
- El registro interno de pg_cron costaba **199 ms de insert + 40 de update** por
  ejecución, mientras el job que registraba tardaba 62 ms. **Anotar costaba 4×
  más que trabajar** — con 96.114 filas acumuladas y jamás purgadas.

Dos reglas que salen de ahí:

1. La frecuencia de una comprobación se fija por **cada cuánto puede cambiar lo
   comprobado**, no por "cuanto más a menudo mejor". Un contador mensual no se
   mira cada 10 minutos.
2. Ese gasto **no escala con los clientes**: crons y polling cuestan lo mismo con
   4 orgs que con 40. Así que se consume el margen ANTES de que entre el primer
   usuario, y cualquier pico añadido tumba la instancia.

Ver [[tablas-de-log-sin-retencion-dominan-el-tamano-de-la-bd]] ·
[[monitor-en-la-misma-infra-no-detecta-su-propia-muerte]]
