---
title: un guard de migración que recalcula la fórmula que asegura se valida a sí mismo
date: 2026-07-25
source: claude-code-session facturaia
tags: [postgres, supabase, migraciones, testing, verificacion]
---

Patrón tentador y vacío: el `DO $$ ... RAISE EXCEPTION` al final de la migración
recalcula a mano la fórmula nueva sobre vectores y la compara con el número
esperado escrito al lado. **Pasa en verde con el cuerpo viejo intacto**: solo
prueba que sabes multiplicar, no que la función/columna quedó bien.

Caso real (mig 564 TuFacturaIA): el guard recomputaba
`COALESCE(cobrable_eur, total) − garantía − aplicado` y lo comparaba con 1060.00.
La migración podía no haber cambiado nada del cuerpo y el guard no se enteraba.

Lo que sí verifica:
- **Inspeccionar el artefacto**: `prosrc`/`pg_get_functiondef` contiene lo nuevo Y
  **no** contiene el patrón viejo (`position('COALESCE(f.total_eur, f.total)' IN v_src) > 0` → EXCEPTION).
  Para columnas generadas, `pg_get_expr` del `attgenerated`.
- **Filas reales**: `count(*) ... WHERE col IS DISTINCT FROM <fórmula>` debe ser 0, y
  las premisas del COALESCE (p. ej. "en recibidas la columna es NULL") también.
- **Dry-run antes de aplicar**: `sed 's/^COMMIT;/ROLLBACK;/'` sobre el fichero y
  ejecutarlo contra prod. Cazó este guard flojo y, de paso, un grant indebido.

Regla: si el guard no puede fallar cuando la migración no hace nada, no es un guard.

Relacionado: [[smoke-prod-en-transaccion-rollback]] · [[postgres-revoke-public-no-elimina-grants-individuales]] · [[defensa-cableada-vs-codigo-muerto]]
