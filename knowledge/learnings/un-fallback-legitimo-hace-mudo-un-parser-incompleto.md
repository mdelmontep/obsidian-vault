---
title: un fallback legítimo hace mudo un parser incompleto — mide la tasa, no el caso
date: 2026-09-09
source: simarro
tags: [parsing, observabilidad, n8n, regex]
---
El sync de Simarro sacaba el agente de la descripción de Idealista con
`/agente?\s*:\s*(...)/gi`: casa `Agente: X`, **no** `Agente Inmobiliario: X`. Ramón usaba las dos
formas, así que 8 de 13 viviendas guardaban `agent = null` → la RPC devolvía `source: "fallback"`
→ la visita se creaba en el calendario general. Nada falla: el fallback es una rama legítima y
diseñada, así que no hay error, ni log rojo, ni alerta. Cuatro meses en el hub como «bloqueante:
Ramón debe añadir `agente:` en Idealista» — el bloqueante era nuestro.

- Un parser cuyo "no encontrado" desemboca en un default correcto **no tiene señal de fallo**. La
  única medida que discrimina es la **tasa**: cuántas filas resuelven sobre el total, no si el caso
  que probaste resuelve. 4/13 y 13/14 se ven idénticos mirando un caso.
- El gate se corre contra el **corpus real** (las descripciones que ya están en la BD, sacadas de
  una ejecución previa), no contra ejemplos inventados: es lo que enseñó que había dos redacciones.
- Cuando el dato lo teclea un humano en un sistema de terceros, asume variantes de redacción y
  cuenta cuántas cubres — antes de escribirle al cliente que rellene mejor su campo.

Ver [[agrupar-ejecuciones-n8n-por-clave-quedate-con-el-id-mas-alto]] ·
[[routing-citas-por-agente]] · [[secreto-con-fallback-literal-degrada-en-silencio-si-falta-la-variable]]
