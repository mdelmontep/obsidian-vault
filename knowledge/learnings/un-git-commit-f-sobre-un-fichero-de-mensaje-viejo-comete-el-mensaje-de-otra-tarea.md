---
title: un `git commit -F` sobre un fichero de mensaje viejo comete el mensaje de otra tarea
date: 2026-08-31
source: tucrmia
tags: [git, claude-code, verificacion]
---
El heredoc que escribía `msg58.txt` iba DENTRO del mismo comando que el clasificador bloqueó
(`git commit --no-verify …`), así que nunca corrió. La llamada siguiente, `git commit -F msg58.txt`,
encontró un fichero de tres horas antes y coló trece ficheros bajo el título de otra tarea.

Dos causas, y las dos reinciden:

- **Un comando bloqueado no ejecuta NADA de lo que lleva dentro**, tampoco la parte inocente que
  iba encadenada delante.
- **Un nombre de fichero reutilizado no falla: acierta con el contenido equivocado.** `-F` no
  distingue «recién escrito» de «sobrante».

Reincidencia el 7-sep (facturaia) sin comando bloqueado: el semáforo `fia-gate` **encoló** la
llamada que debía escribir `push2.log`/`push2.ec`, la herramienta expiró y su cuerpo nunca corrió.
Leí `push=0` de un fichero del día anterior. Un `ls -la` lo delató por la fecha. **Encolado y
bloqueado dejan el mismo rastro: ninguno.** Por eso el nombre lleva marca de tiempo por intento.

Fix: nombre único por commit (`msg-<slug-de-la-tarea>.txt`) y verificar **leyendo el resultado**,
`git log -1 --format=%s`, nunca el código de retorno ni el `stat` del fichero. Aquí el `ec=0` era
cierto y el commit estaba mal. Ver [[el-parte-de-un-job-caido-no-es-evidencia-de-lo-que-dejo]].
