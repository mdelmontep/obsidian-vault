---
title: clasifica el rojo de CI contando pasos ejecutados, y fecha la frontera antes de hablar de causas
date: 2026-08-05
source: claude-code-session
tags: [ci, github-actions, metodo, verificacion]
---
«El CI está en rojo» no es una causa. La discriminación más barata no es leer el log: es **contar pasos
ejecutados** por la API — `gh api repos/O/R/actions/runs/<id>/jobs --jq '.jobs[]|[.steps[]]|length'`

- **0 pasos** → el job nunca arrancó. Rojo estructural, no dice nada del diff, y **no hay log que mirar**:
  una regla del tipo «confirma que es el flake conocido» es inaplicable aquí.
- **≥1 paso, 0 tests fallidos** → flake de infraestructura (teardown, BD efímera).
- **≥1 paso, ≥1 test fallido** → **rojo REAL**, el que una doc mal escrita hace ignorar.

⚠️ **Corrección del 05-ago, y es la parte que costó:** esta nota decía «hay DOS causas conviviendo», a
partir de dos runs del mismo día (uno de 13 pasos, otro de 0). **Falso.** Recorriendo la serie completa
salieron **12 runs consecutivos a 0 pasos**, con frontera exacta —el último que ejecutó algo fue el 04-ago
22:38:58, justo el de 13 pasos que se citaba de contraste— y la anotación literal: *«The job was not
started because recent account payments have failed»*. Es **una sola causa con fecha de inicio**.

**Por qué el marco importa más que el dato:** con «dos causas» se buscan dos arreglos; con «un antes y un
después» se mira *Billing* y se acaba. **Dos runs no son una serie** — fecha la frontera antes de nombrar
causas. Corolario: si el CI monta la BD real es la **única** superficie que corre los tests que el gate
local autosalta sin base de datos (medido: 226 skips con BD, **423** sin ella).
