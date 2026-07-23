---
title: si la suite empeora tras un bump, comparar contra origin/main limpio antes de culpar al bump
date: 2026-07-23
source: claude-code-session — FacturaIA PR #1177 (sharp/next CVE)
tags: [testing, ci, methodology, regression]
---
Al bumpear `next` 16.2.9→16.2.11 en un repo donde main avanzaba en paralelo
(6 commits de otro trabajo mergeados durante la sesión), la suite completa
pasó de 94 a ~306 tests fallando. Conclusión inmediata (equivocada): "el bump
de next rompe algo". Causa real: el baseline de 94 se había medido en un
commit de main más viejo, ANTES de que aterrizara ese otro trabajo (migración
a Cache Components) que ya traía ~207 fallos nuevos de fábrica, sin relación
con next.

Verificación correcta: `git worktree add` desde `origin/main` puro (sin
ningún cambio propio) y correr la suite ahí. Si el número ya está mal en
limpio, el bump no es el culpable — hazlo apples-to-apples reinstalando
ambas versiones sobre la MISMA base y comparando (aquí: 314 fallos idénticos
con next 16.2.9 y con 16.2.11, mismo desglose exacto).

Regla: nunca atribuyas una regresión de suite a tu cambio sin haber corrido
la misma suite en la base sin tu cambio, en la MISMA punta de main. Un
baseline viejo es indistinguible de una regresión nueva si no controlas la
variable de qué commit de main estabas usando.
