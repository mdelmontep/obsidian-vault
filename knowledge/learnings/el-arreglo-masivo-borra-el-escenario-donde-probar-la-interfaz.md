---
title: el arreglo masivo borra el escenario donde ibas a probar la interfaz
date: 2026-08-22
source: facturaia
tags: [qa, smoke, orden-de-trabajo]
---

Cuando el mismo trabajo trae (a) un barrido que repara los datos rotos y (b) la interfaz para que el
usuario los arregle a mano, ejecutar el barrido primero deja la interfaz **sin ningún caso real donde
probarse**. Y es justo la parte que el usuario va a ver.

Caso real (TuFacturaIA, #2089): tras correr el barrido, las 26 filas congeladas pasaron a 0. La
acción masiva del listado y el botón de un clic de la ficha se quedaron sin sujeto; el bloque del
panel solo se pudo verificar montando a mano un caso en una organización `is_test`, con una divisa
sin cobertura, y devolviéndola después a su estado.

- **Orden correcto**: smoke de la interfaz sobre los datos rotos → barrido → smoke de que quedó
  reparado. Dos pasadas, no una.
- Si ya reparaste, **monta el caso en sandbox y devuélvelo**: es más honesto que declarar «cubierto
  por tests» sobre lo que el usuario toca.
- Ese smoke fue el que encontró los dos defectos de precisión que nadie había visto (#2090) y el
  contraste ilegible (#2091): la prueba en vivo **después** del arreglo grande no es trámite.
