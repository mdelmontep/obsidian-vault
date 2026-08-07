---
title: registrar una migración sin ejecutarla envenena la BD para siempre
date: 2026-08-07
source: claude-code-session
tags: [migrations, postgres, integridad, tests, gate]
---
Un bootstrap que aplica el `schema.sql` de HEAD y **marca todas las migraciones como aplicadas** es
correcto sobre una base NUEVA y una mentira sobre una que ya existe: ahí el `CREATE TABLE IF NOT
EXISTS` no toca los objetos viejos, pero el registro sí se escribe. Desde ese momento el migrador las
**salta para siempre** y la base queda **irreparable por el camino documentado**.

AGH 7-ago, medido: `agh_dev` con las 33 migraciones REGISTRADAS y el CHECK de `audit_log` con 12
valores en vez de 15. `npm run db:migrate` responde «migraciones aplicadas» y **no cambia nada**.

- Se propaga solo: si los tests llaman al bootstrap contra lo que apunte `DATABASE_URL`, **cualquier
  base de vida larga se envenena** la primera corrida tras una migración nueva. Síntoma: rojos que
  parecen de tu diff.
- Por eso **`schema_migrations` no sirve para responder «¿está al día?»**. Hay que preguntar al
  esquema REAL — comparar la constraint viva contra la que declara el `schema.sql`, que es HEAD por
  construcción si hay drift-gate. Sin escribir una segunda lista, que divergiría.
- Salida: `dropdb` + `createdb` + migrar. Y el mensaje del guard **no debe decir el comando que no
  repara**, o cuesta otra corrida a quien lo lea.

Relacionado: [[schema-migrations-no-es-source-of-truth-si-aplicas-manual]] ·
[[migraciones-incrementales-conviviendo-con-schema-sql-guarded]]
