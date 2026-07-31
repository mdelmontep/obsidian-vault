---
title: un test que re-aplica una migración congelada ESTRECHA lo que otras ampliaron
date: 2026-07-31
source: claude-code-session
tags: [testing, postgres, migraciones, flaky, agh-iberica]
---

Patrón: `schema.sql` (bootstrap idempotente) + migraciones numeradas. Como
`CREATE TABLE IF NOT EXISTS` **no re-crea los CHECK** sobre una BD vieja, un test
"compensa" re-aplicando a mano la migración que los amplió. Ese compensador
**envejece**: la migración congelada fija el CHECK a los N valores de su día, y
cada migración posterior que lo amplía deja al test estrechándolo.

Lo que lo hace invisible: el `catch` del bootstrap iguala «no conecta» con «el
schema falló» → el fichero entero degrada a *skip* y la suite dice *passed*. El
fallo sale luego en OTRO test que audite una entidad de las que faltan, y en
sitios distintos según el orden de ficheros → se lee como «el gate oscila».

Fix: nadie predice el estado del SQL. Arrancar por el camino REAL de producción
(fresca → `schema.sql`; existente → solo migraciones). El sondeo de conectividad
decide el skip; el bootstrap va **fuera** de ese `catch` y falla ruidosamente.

**Corolario caro: impedir ≠ curar.** Quitar el re-aplicado evita envenenar más
BD, pero las ya estrechadas **no se reparan solas** — con `schema_migrations`
completa no hay nada pendiente que aplicar. Hace falta una migración nueva que
re-afirme la constraint; es lo único que llega por el arranque a todas las
máquinas y a prod. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].
