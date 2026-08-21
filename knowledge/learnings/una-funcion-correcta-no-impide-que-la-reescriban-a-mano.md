---
title: una función correcta ya escrita no impide que la reescriban a mano
date: 2026-08-21
source: facturaia
tags: [guards, refactor, testing]
---
`cuotaIvaCabecera` existía, trataba bien la retención y la ficha ya la usaba. Aun
así tres sitios volvieron a escribir `total − base` al lado. En una recibida con
retención el total se guarda neto, así que esa resta da `cuota − retención`:
pintaba 87 € donde eran 304,50.

El fallo no fue no tener la función. Fue que la resta es **más corta de escribir
que de buscar**, y nada la paraba. Un cuarto sitio la habría escrito igual.

Patrón: cuando un cálculo con sesgo tiene ya su fuente única, el arreglo no es
solo sustituir las copias — es un **guard sobre el PATRÓN**, barriendo el módulo
con `git ls-files` y un regex, no una lista de ficheros a mano. Y probarlo por
mutación: reintroduce la resta y el test tiene que caer.

Alcance declarado > lista blanca: lo que no da tiempo a arreglar va a un issue,
no a las excepciones permitidas. Una excepción con motivo se lee como «revisado
y correcto». Ver [[backfill-guardado-por-invariante-en-vez-de-por-sintoma]].
