---
title: un gate anclado a un diseño no desplegado falla idéntico contra todo y deja de medir
date: 2026-09-09
source: centro-elphis
tags: [gates, harness, testing, anti-patron]
---
`gate.py` se reescribió el 7-sep para dejar de bloquear el diseño de la Fase 4 y se le puso ese
diseño (`flow-P6.json`) como línea base. P6 nunca se publicó. Resultado medido el 9-sep:
**exit=1 con los mismos 33 fallos contra v37, contra v44 y contra v45**.

**La prueba de que un gate no discrimina es que dé el mismo resultado contra versiones
distintas** — más barata que la mutación y no hace falta tocar nada. Un rojo permanente se
ignora, y a partir de ahí el gate no protege de nada: el mismo fallo que motivó su reescritura.

Resnapshotear a producción sin más habría borrado un requisito de negocio pendiente. La salida
es **dos categorías con dos salidas**: `check()` mide contra producción y bloquea; `deuda()`
lista las propiedades del diseño futuro que producción no cumple y no bloquea. El día que se
despliegue, cada `deuda()` pasa a `check()`.

Corolario: al reanclar la base, verifica **qué requisito estabas codificando en la base vieja**.
Aquí la cabecera afirmaba un requisito del cliente («cero transferencias») que no aparece en
ningún otro sitio del vault y que contradice una decisión firmada. Un gate no es sitio para
guardar la única copia de una decisión de negocio.

Ver [[un-mutante-que-no-muerde-puede-no-haber-mutado-nada]]
