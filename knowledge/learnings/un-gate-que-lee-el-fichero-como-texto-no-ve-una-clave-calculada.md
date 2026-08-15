---
title: un gate que lee el fichero como texto no ve una clave calculada, y tiene razón
date: 2026-08-15
source: claude-code-session
tags: [gates, catalogos, tucrmia]
---
Doce entradas nuevas de un catálogo había que declararlas «pendientes con motivo». Escribirlas
con un `...Object.fromEntries(lista.map(...))` compila, tipa y **el gate las siguió contando
como huérfanas**: lee el fichero como TEXTO y casa `clave: 'motivo'`, así que unas claves
calculadas le son invisibles.

No es una limitación a rodear — es la condición que le permite **exigir el motivo**: para
comparar prosa contra una clave tiene que leer el fuente, no importar el módulo. Un gate que
importara el catálogo vería las doce claves y no podría decir si el motivo está escrito o es
una cadena vacía generada.

Fix: escribirlas a mano, una por línea, con motivo propio cada una — que además es lo que la
cabecera del propio fichero pedía («cada fila dice POR QUÉ, no sólo QUE»).

Regla: antes de compactar una lista declarativa, mira **quién la lee**. Si la lee un gate por
texto, la forma corta la apaga en silencio.

Ver [[dos-trampas-al-escribir-un-gate-por-arbol-de-sintaxis]] · [[bloque-generado-para-gate-byte-a-byte-nunca-se-transcribe-de-memoria]]
