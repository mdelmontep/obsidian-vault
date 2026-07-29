---
title: "compiló" no es "terminó": el tail del log de next build engaña
date: 2026-07-29
source: claude-code-session
tags: [nextjs, verificacion, gate, metodo]
---

`next build` imprime `✓ Compiled successfully in N min` y DESPUÉS corre la
pasada de TypeScript y el page-data, que tardan tanto o más. Mirar la cola del
log en ese punto da un check verde que no es el del final.

Caso real: di por bueno un build así y el push lo rechazó el hook; peor, había
mirado la medición de la misma forma y se me coló que arrastrar una columna
para estrecharla ya no funcionaba (la medida decía 630 px con 340 declarados y
lo dejé pasar porque "ya no recortaba").

Espera al marcador del FINAL (la leyenda de rutas: `server-rendered on demand`)
o al fin del proceso por PID, nunca a un `✓` intermedio:

```bash
nohup npm run build > build.log 2>&1 & PID=$!
while kill -0 $PID 2>/dev/null; do sleep 10; done   # no `pgrep -f "next build"`
grep -E "server-rendered on demand|Failed to compile|error TS" build.log
```

Corolario: una cifra que no cuadra con lo declarado es un fallo aunque el
síntoma que perseguías haya desaparecido.
Ver [[el-bucle-que-espera-con-pgrep-se-encuentra-a-si-mismo]].
