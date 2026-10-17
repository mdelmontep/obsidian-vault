---
title: set role o reset role dentro de una migración rompe el db push de prod
date: 2026-10-17
source: facturaia (mig 1085, PR #3653)
tags: [supabase, migraciones, postgres]
---
- **Qué pasa:** la 1085 verificaba sus políticas con `SET ROLE authenticated … RESET ROLE`. En local y en staging pasaba, pero el `supabase db push --linked` de prod abortó con `42501`.
- **Por qué:** el CLI se conecta con un rol de login temporal. `RESET ROLE` vuelve a ese rol, no a `postgres`, así que el resto de la migración corre sin los permisos con que empezó.
- **Fix:** comprobar sin cambiar de rol. Leer el catálogo (`pg_policies`, `has_function_privilege('authenticated', …)`) y lanzar una excepción si no cuadra. Candado en facturaia: `scripts/__tests__/migraciones-sin-cambio-de-rol.test.ts`.
- **Regla:** una migración no cambia de rol. La prueba «como authenticated» va en un test de integración, no en el SQL que se aplica.
