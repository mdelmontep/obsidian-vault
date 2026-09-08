---
title: matar el envoltorio no mata el proceso que hace el trabajo
date: 2026-09-08
source: facturaia
tags: [procesos, git, hooks, verificacion]
---
Lanzas un gate como `nohup zsh -c 'git push …' &`, matas el `zsh` para soltar la
máquina, lo ves desaparecer y das el turno por libre. El `git push` sigue vivo
bajo otro pid con su `pre-push` dentro, comiéndose CPU y base compartida.
**El envoltorio solo lanza; el trabajo está en el hijo**, que sobrevive al padre:
que el wrapper no salga en `ps` no dice nada del proceso que importa.
Verifica por el trabajo y baja por los hijos: `pgrep -fl 'git push'` (el comando
real, no el zsh) y `ps aux | grep <ruta-del-worktree>` (quién corre DENTRO).
El mismo día apareció un `test:integration` con el padre ya muerto martilleando
la base compartida: superviviente de un push «matado» horas antes.

Opuesto: [[matar-un-proceso-no-lo-para-si-detras-hay-un-servicio-que-lo-resucita]]
