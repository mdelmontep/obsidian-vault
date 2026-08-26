---
title: el bucle que espera con pgrep se encuentra a sí mismo
date: 2026-07-29
source: claude-code-session
tags: [bash, verificacion, harness]
---

`until ! pgrep -f "next build"; do sleep 10; done` no termina nunca: el patrón
está en la línea de comandos del propio shell que ejecuta el bucle, así que
`pgrep -f` se encuentra a sí mismo. Peor que colgarse: al preguntar "¿sigue
corriendo?" respondes que sí mirando tu propio proceso, y das por vivo un build
que terminó hace rato.

Fix — filtra por el binario real, no por la cadena:

```bash
pgrep -fl "next build" | grep -v "pgrep\|until\|zsh -c"
# o mejor: guarda el PID al lanzar y espera por él
nohup npm run build > build.log 2>&1 & PID=$!
while kill -0 $PID 2>/dev/null; do sleep 10; done
```

Y no solo a sí mismo: casa con los shells de OTRAS sesiones que esperan a lo
mismo (26-ago, dos direcciones el mismo día). `pgrep -q -f "npm run gate"` dio
«sigue corriendo» durante 20 min sobre un gate terminado, porque una sesión
paralela tenía su propio `until ! pgrep -f "npm run gate"` vivo; y un
`pkill -f "next build"` mató el shell de vigilancia de otra sesión. Con varias
sesiones en el mismo repo, el patrón no identifica un proceso: identifica una
frase escrita en muchas líneas de comandos.

Regla general: un `pgrep -f` sobre una cadena que tú mismo acabas de escribir en
un comando es siempre sospechoso. Vale igual para `ps aux | grep`.
Ver [[sondear-la-capacidad-real-no-la-presencia-del-binario]].
