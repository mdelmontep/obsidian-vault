---
title: un candado que el issue pide puede cegar a otro consumidor, y lo caza el gate y no la revisión
date: 2026-08-17
source: claude-code-session
tags: [testing, invariantes, revision, metodo]
---

Un issue puede pedir un candado con toda la razón aparente y que ese candado **no pueda existir**.
Antes de implementar una invariante del tipo «X es imposible, así que niégalo», hay que **contar los
consumidores de la función y preguntarle a cada uno si X significa algo para él**.

Caso medido (AGH #1291). El issue pedía: *«la línea del gate debe ser INCAPAZ de decir `0 passed` con
ficheros en verde — es una invariante cruzada, no un caso más»*. Se implementó tal cual y **el gate la
puso en rojo**: esa combinación era el **diagnóstico** de otro consumidor.

```
Test Files 1 passed · Tests 0 passed (0)   arnés roto: el fichero pasa sin ejecutar aserciones
Test Files 1 failed · Tests 0 passed (0)   el mutante ni compila: revienta al importar
```

La segunda formulación, más fina y sobre la firma exacta del defecto, **también** era un diagnóstico
suyo. El candado que «cerraba» el issue habría convertido dos señales distintas en un «no pude leerlo».

- **Un valor raro no es ruido por ser raro**: puede ser la única señal que alguien tiene. Una
  invariante se escribe mirando al productor y se paga en los consumidores.
- **El error de método fue barato**: se afirmó «sólo X consume esta función» tras un grep cuyo segundo
  resultado no se leyó. Lo cazó el gate, no la revisión.
- **Si el candado no puede existir, decirlo en el código y en la PR con la medición**, y dejar casos
  que aseveren **lo contrario** de lo que pedía el issue, para que nadie lo cierre otra vez por ahí.
- El defecto real suele seguir siendo arreglable donde estaba, y **ése sí admite candado** — pero
  comprueba que la pieza que arregla está atada: un arreglo con dos piezas redundantes deja una sin
  cubrir y nada avisa. Ver [[una-mutacion-sin-victima-puede-ser-el-arnes]].

**La pregunta que discrimina (18-ago, dos issues el mismo día pidiendo el mismo candado y sólo uno
posible): ¿el SUJETO del patrón tiene dueño único?** `mock.calls[0]!` (#1327) **sí** — `.mock` la crea
la librería: ningún fixture puede tenerla ni ningún espía evitarla, así que prohibirla es exacto. «Toda
lectura de `entries` pasa por el helper» (#1334) **no** — un fixture puede llamar así a su campo y un
grabador puede no usarlo (**dos colisiones vivas** medidas antes de escribir una línea). Los dos se
escriben igual —un grep prohibitivo— y sólo uno es invariante: cuenta consumidores **y** pregunta de
quién es el nombre. Si no puede existir, **declararlo con la medición ES la entrega**.
