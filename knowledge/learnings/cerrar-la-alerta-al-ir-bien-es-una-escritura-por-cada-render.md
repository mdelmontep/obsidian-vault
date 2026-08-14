---
title: «si fue bien, cierra la incidencia» en un camino caliente es una escritura por cada render
date: 2026-08-14
source: claude-code-session
tags: [observabilidad, alertas, rendimiento, supabase]
---

Al darle cierre automático a una alerta se escribe lo obvio: si la lectura falló, emitir;
si fue bien, resolver. En un cron da igual. En un layout de dashboard significa **un RPC de
escritura por cada visita de cada usuario**, para cerrar algo que casi nunca está abierto.

No lo caza ningún gate ni se ve en el TTFB, porque suele ir fire-and-forget. Lo que lo
delata es preguntarse «¿cada cuánto corre esta línea?» al releer el diff, no si compila.

Fix: throttle por clave en memoria del proceso (una vez cada 10 min basta). Y **no**
condicionarlo a que sea esta instancia la que abrió la alerta: con varios procesos, el que
abre no tiene por qué ser el que la vea recuperarse, y atarlo a eso deja alertas colgadas
para siempre — que es el fallo que el cierre automático venía a evitar.

Complementario de [[alerta-que-se-resuelve-al-volver-a-funcionar-queda-huerfana-si-su-sujeto-desaparece]]:
aquel es cuándo NO se cierra nunca; este es cuánto cuesta cerrarla de más.
