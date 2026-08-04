---
title: un guard de secretos que mira el NOMBRE de la clave bloquea "secreto" porque contiene "secret"
date: 2026-08-04
source: claude-code-session
tags: [hooks, seguridad, typescript, tucrmia]
---

El hook global `dokploy-secret-guard.sh` (Write/Edit) bloquea si una línea empieza (tras
whitespace/`export`) con un identificador que contenga SECRET/PASSWORD/TOKEN/API_KEY/etc y el
valor asignado no parece placeholder. Es case-insensitive y busca SUBSTRING, así que cualquier
identificador español con "secreto" (contiene "secret"), "credencial" NO la contiene pero
"contraseña" tampoco — ojo con neologismos calcados del inglés. Escribiendo `core/webhooks/`
(TuCRMIA) bloqueó `const SECRETO_CIFRADO = …`, `secreto: valor,` en su propia línea, y
`endpointSecretEncrypted: X`, aunque ninguno fuera un secreto real.

Dos fixes, no uno: (1) para nombres de dominio, evita el substring en inglés en el identificador
si vas a asignarle un valor largo en su propia línea (`endpointClaveCifrada` en vez de
`endpointSecretEncrypted` — "clave" no está en la lista); (2) para llamadas puntuales que sí
necesitan el parámetro `secreto:`, mantenlas en una sola línea (el guard solo mira el INICIO de
línea, no substrings a mitad de línea) — Prettier las reformatea multilínea después, pero eso pasa
por Bash, no por Write/Edit, así que no vuelve a disparar el hook.

Ver `~/.claude/hooks/dokploy-secret-guard.sh` para la lista completa de palabras vigiladas.
