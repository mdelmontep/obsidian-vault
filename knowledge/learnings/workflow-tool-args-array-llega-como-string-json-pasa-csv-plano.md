---
title: el parámetro args del tool Workflow, pasado como array JSON, llegó al script como string
date: 2026-08-04
source: claude-code-session — auditoria-composicion.js de tucrmia
tags: [claude-code, workflow, tooling, gotcha]
---

Invocar `Workflow` con `args: ["a", "b", "c"]` (array JSON real en la llamada al tool, no una
cadena) hizo que el script recibiera `args` como el STRING `'["a","b","c"]'` — no como array.
El script tenía el fallback correcto (`typeof args === 'string' ? args.split(',') : []`), pero
como el string traía corchetes y comillas, el split produjo claves corruptas
(`'["a"'`, `' "b"'`, …) y el guion se paró con `lente_desconocida` sin gastar un solo agente:
protección correcta, síntoma confuso.

Reproducido dos veces el 4-ago (con y sin `resumeFromRunId`) y otra vez el 5-ago en la misma
auditoría de composición de TuCRMIA — recurrente, no un fallo puntual.

**Workaround que funcionó**: pasar `args` como un STRING plano separado por comas
(`"a,b,c"`, sin corchetes ni comillas) en vez de un array — el propio fallback del script lo
parte bien. Si el script que vas a lanzar espera un array de claves simples, prueba primero con
la forma de string plano si el array da `lente_desconocida`/similar sin gastar agentes.
