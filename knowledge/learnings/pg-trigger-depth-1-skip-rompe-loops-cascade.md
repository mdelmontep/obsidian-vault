---
title: pg_trigger_depth() > 1 SKIP rompe loops cascade sin flag de sesión
date: 2026-05-21
source: claude-code-session
tags: [postgres, triggers, loops]
---

Triggers entrelazados entre tablas (A → B → A) entran en loop infinito
cuando cada uno actualiza la otra y dispara cascada. Caso clásico:
recompute_factura_estado (en mfa) → UPDATE facturas → mirror (en
facturas) → INSERT/UPDATE mfa → recompute → ...

Fix estructural simple: añadir guard al inicio del trigger problemático:
```sql
IF TG_OP = 'UPDATE' AND pg_trigger_depth() > 1 THEN RETURN NEW; END IF;
```

`pg_trigger_depth()` devuelve el nivel de anidamiento. depth=1 =
operación inicial del user. depth>1 = estamos dentro de cascade. El
trigger sigue ejecutándose en su uso "inicial" (auto-match al INSERT
factura/mov) pero no en cascadas (UPDATE estado por recompute).

Más limpio que flags de sesión (`current_setting('app.in_chain')`) y
no requiere refactor de funciones llamantes. Aplicar a TODOS los
triggers de la cadena por defensa-en-profundidad — no basta cerrar
una rama si hay otras (caso FacturaIA mig 140: 2 de 4 triggers
auto-mark protegidos, los otros 2 quedaron expuestos hasta mig 141).

Complementa [[trigger-recursivo-revertir-estado-deja-candidato-libre-que-otro-trigger-rematchea]]: ese learning describe el síntoma, este es la solución estructural.
