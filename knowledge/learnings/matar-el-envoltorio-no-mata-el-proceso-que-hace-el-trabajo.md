---
title: matar el envoltorio no mata el proceso que hace el trabajo
date: 2026-09-08
source: facturaia
tags: [procesos, git, hooks, verificacion]
---
Lanzas un gate como `nohup zsh -c 'git push …' &`, matas el `zsh` para soltar la
máquina, lo ves desaparecer y das el turno por libre. El `git push` puede seguir
vivo bajo otro pid con su `pre-push` dentro, comiéndose CPU y base compartida.

**Pero no siempre, y esa es la corrección** (8-sep-2026, los dos casos el mismo
día): una vez el hijo sobrevivió al padre; otra, el kill alcanzó al grupo entero
y se llevó el push a mitad del gate. Ni «murió» ni «sigue vivo» se deducen de que
el wrapper desaparezca — son **dos hipótesis, y hay que medir cuál**.

Veredicto por dos medidas de naturaleza distinta, nunca por una:
- El PROCESO: `pgrep -fl 'git push|vitest|next build'`, el comando real y no el zsh.
- El EFECTO: `git ls-remote origin <rama>` contra `git rev-parse HEAD`, y si el log
  del gate sigue creciendo (`stat` del fichero con un minuto de diferencia).

Log congelado + sin proceso + sin rama en el remoto = murió, relanza. Con
cualquiera de las tres al revés, sigue vivo: no relances o duplicas el push.
Para que el kill del envoltorio NO se lo lleve, lanzar desacoplado (`nohup` a un
script propio + `disown`), no como hijo directo del comando del turno.

Opuesto: [[matar-un-proceso-no-lo-para-si-detras-hay-un-servicio-que-lo-resucita]]
