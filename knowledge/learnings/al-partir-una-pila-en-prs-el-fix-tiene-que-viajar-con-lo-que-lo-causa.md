---
title: al partir una pila en PRs, el fix tiene que viajar con el commit que causa el fallo
date: 2026-08-03
source: claude-code-session
tags: [git, pr, privacidad, rgpd]
---
Cuando una rama larga se parte en varios PRs por tema, el corte se hace por *asunto*
—«esto es visual, esto es contenido»— y un fix posterior se queda en el PR de la otra mitad.
Mergear el primero publica el fallo, y el arreglo llega días después. Con datos personales o
secretos, el hueco entre los dos merges es la exposición.

Regla: antes de partir, `git log --oneline <rango>` buscando commits que **arreglen** a otro
del mismo rango. Cada fix se cherry-pickea al PR que contiene su causa, no al que le toca por
tema. Y decirlo en la descripción: «no mergear los N primeros por separado».

Caso real (agentesia-web, 03-ago): 4 commits en `main` local publicaban audio de llamadas
reales; el commit que quitaba los nombres de cliente de esos audios vivía en OTRA rama, la del
rediseño. Mergear el PR de contenido tal cual sacaba nombre y apellidos a producción. Ver
[[los-audios-de-llamadas-reales-llevan-nombres-de-clientes]] ·
[[pr-encadenada-se-mergea-en-su-base-si-no-borras-la-rama]]
