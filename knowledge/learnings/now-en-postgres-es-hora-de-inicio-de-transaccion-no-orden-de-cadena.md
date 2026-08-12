---
title: ordenar por created_at una cadena serializada con advisory lock puede darte el orden contrario
date: 2026-08-12
source: claude-code-session
tags: [postgres, concurrencia, verifactu, integridad]
---

`now()` en Postgres es la hora de **inicio de transacción**, no del instante. Si
una cadena de registros se serializa con `pg_advisory_xact_lock` pero se ordena
después por `created_at`, los dos órdenes pueden contradecirse:

- Tx A empieza en t1, Tx B en t2 > t1.
- B coge el lock primero, encadena y commitea. A entra después y encadena
  DETRÁS de B (correcto).
- Pero `created_at` dice A (t1) antes que B (t2): el orden inverso al de la cadena.

Con cadenas fiscales (VeriFACTU) eso significa enviar los registros fuera de
orden y romper el `RegistroAnterior` en destino.

**Patrón**: si el orden importa, persiste la posición DENTRO del mismo lock que
lo decide (`ultima_pos + 1`), con índice único parcial `(ambito, pos)` como
candado, y ordena por ella. Nunca la infieras de una marca de tiempo.

Y si además hay un timestamp que debe ser coherente con la cadena, usa
`clock_timestamp()` (instante real, dentro del lock), no `now()`.

Caso: FacturaIA mig 663, `facturas.verifactu_cadena_pos`.
