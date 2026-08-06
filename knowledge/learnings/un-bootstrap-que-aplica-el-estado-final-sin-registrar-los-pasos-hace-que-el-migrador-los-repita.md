---
title: un bootstrap que aplica el esquema final sin registrar las migraciones hace que el migrador las repita
date: 2026-08-07
source: claude-code-session
tags: [postgres, migraciones, testing, gate]
---
`applySchema(pool)` aplicaba `schema.sql` —el estado FINAL, ya consolidado— y **no escribía
`schema_migrations`**, ni creaba la tabla. Así que la base quedaba al día pero **sin decirlo**, y el
primer migrador que la tocara re-aplicaba **todas** las migraciones sobre un esquema que ya las
contenía.

La mayoría son idempotentes y no se nota **nunca**, hasta que una no lo es: aquí la 0028 reafirmaba
un CHECK con 12 valores, sin los 2 que añadía la 0031, así que su `ALTER TABLE` revalidaba la tabla
y reventaba con `23514` contra filas perfectamente legales. Se llevó por delante un gate entero —10
ficheros sin ejecutar un test— y **el síntoma apuntaba al diff de quien pasara por ahí**, no a la
causa.

**Fix: registrar, no ejecutar.** Tras aplicar el esquema, insertar todas las migraciones en la tabla
de control (`ON CONFLICT DO NOTHING`), con el **mismo** calculador de checksum que usa el migrador —
si se calcula aparte, la siguiente corrida las ve «modificadas tras aplicarse» y aborta. Se sostiene
en que un drift gate garantice que el esquema es el consolidado.

Alternativa peor: hacer idempotente la migración culpable. Tapa el síntoma de una, no cierra la clase.
