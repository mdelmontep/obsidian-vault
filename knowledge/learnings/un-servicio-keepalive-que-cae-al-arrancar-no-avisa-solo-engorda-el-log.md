---
title: un servicio keepalive que cae al arrancar no avisa, solo engorda el log
date: 2026-10-17
source: learn-agentesia (runner del Aula, LaunchAgent es.agentesia.aula.runner-remoto)
tags: [launchd, macos, observabilidad, servicios]
---
Un LaunchAgent con `KeepAlive` cuyo proceso muere al arrancar (dependencia que falta, config rota) no se
ve caído: launchd lo relanza cada ~10 s, `launchctl list` lo muestra con pid casi siempre y lo único que
cambia es el log. Caso real: runner del Aula, 3 días y 24.347 `ERR_MODULE_NOT_FOUND` (31 MB) sin que
nadie lo notara; el síntoma era que no salían lecciones.

- Diagnóstico rápido: `launchctl list | grep <label>` → la 2.ª columna es el último exit (≠0 = está cayendo);
  `ps -o lstart -p <pid>` dice si el pid es de hace segundos.
- Prevención: `ThrottleInterval` alto en el plist y un aviso cuando hay N salidas seguidas ≠0 (o un
  latido que el propio servicio escribe y otro vigila).
- Tras arreglarlo, medir por posición del log (`wc -l` antes, `tail -n +N` después), no por su tamaño.
Relacionado: [[matar-un-proceso-no-lo-para-si-detras-hay-un-servicio-que-lo-resucita]] · [[aula]]
