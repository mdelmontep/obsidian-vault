---
title: Cadena hash encadenada Postgres requiere advisory_xact_lock por partición
date: 2026-05-18
source: claude-code-session
tags: [postgres, verifactu, race-condition, trigger, gotcha]
---

Trigger BEFORE INSERT que calcula huella encadenando con la anterior (Verifactu, audit trail, blockchain-like): 2 INSERTs concurrentes en la misma partición leen la misma huella anterior y commitean ambos → cadena rota silente. `SELECT...LIMIT 1` con `FOR UPDATE` no basta: la fila nueva aún no existe.

Fix: advisory lock por partición lógica.

```sql
PERFORM pg_advisory_xact_lock(
  hashtextextended('cadena:' || partition_key, 0)
);
```

Liberación auto al COMMIT. Coste ~5µs. `hashtextextended` retorna BIGINT estable. Patrón universal para cualquier cadena hash en Postgres.
