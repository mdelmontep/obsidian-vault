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

Regla general: un `pgrep -f` sobre una cadena que tú mismo acabas de escribir en
un comando es siempre sospechoso. Vale igual para `ps aux | grep`.
Ver [[sondear-la-capacidad-real-no-la-presencia-del-binario]].
