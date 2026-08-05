---
title: el delimitador se elige contra el dato real, no a gusto tipográfico
date: 2026-08-05
source: claude-code-session
tags: [seguridad, prompt-injection, metodo, delimitadores]
---
Al acotar dato no confiable —contexto de un prompt, parámetro de plantilla, valor en una consulta— la marca
se elige **grepeando qué contiene ya el dato real**, no por gusto. Iba a envolver labels de entidad con
`«…»` y los productores (`opportunities-read-tool.ts`) **ya emitían `«${title}» de ${cliente}`**: la marca
habría sido indistinguible del contenido justo en el caso más común.

Una delimitación cuya marca aparece dentro del valor **no delimita nada**, y falla en silencio: se lee bien
en el ejemplo que escribes tú y se rompe con los datos de producción.

Dos mecanismos, y hacen falta los dos:
- **neutralizar la marca de cierre** dentro del valor — si no, basta escribirla para salirse y seguir dando
  instrucciones fuera (es *el* ataque contra una marca ingenua);
- **colapsar el espacio en blanco** — sin esto un `\n` dentro del dato fabrica una línea nueva que se lee
  como estructura del propio prompt.

El candado que lo prueba es determinista y gratis: un valor hostil que intenta cerrar la marca, y un valor
legítimo que contiene la marca descartada. En prompts, ojo al efecto colateral que los tests no ven: el
modelo puede **copiar la marca dentro del valor que emite** → sondéalo con un fichero de evals antes de la
corrida completa. Y precisa el diagnóstico: si el dato lo escribió **otro usuario** de un store compartido
por diseño, es **inyección, no fuga** — leído como fuga el arreglo sería re-scopear, y el correcto es acotar.
