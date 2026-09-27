---
title: reconciliar por ausencia cierra en falso lo que un detector no pudo leer
date: 2026-09-27
source: facturaia
tags: [monitorizacion, alertas, detectores]
---
Patrón: un barrido abre incidencias con lo que sale rojo y **resuelve todo lo abierto que no ha salido** esta pasada.
Gotcha: si un detector falla al leer y devuelve `[]` («no puedo afirmar nada»), para el barrido es «todo recuperado»: cierra sus incidencias, y la pasada siguiente las reabre y **reenvía el email**. Un `null` bien distinguido dentro del detector no basta si el que reconcilia no recibe esa distinción.
Fix: el detector señala «no evaluado» (lanza o devuelve una marca) y el barrido añade sus prefijos a la lista de no evaluados, igual que con los que se salta por coste. Ausente-porque-no-se-miró ≠ recuperada.
Caso: facturaia, collector `ventas-sin-descontar-stock` (27-sep-2026), el mismo hueco en otros dos detectores de stock anteriores. Lo cazó `/fia-cierre`, no los tests.
Relacionado: [[ausencia-de-consumidor-no-es-ausencia-de-funcion]]
