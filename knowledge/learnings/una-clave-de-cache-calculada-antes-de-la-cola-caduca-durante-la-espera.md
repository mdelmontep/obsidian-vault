---
title: una clave de caché calculada antes de la cola caduca durante la espera
date: 2026-09-24
source: facturaia
tags: [cache, gates, concurrencia, pre-push]
---
En la caché de verdes del `pre-push` (#2928), la clave de cada etapa incluía la huella de la base local compartida. Esa clave se calculaba **antes** de pedir plaza al semáforo, y la cola duraba más de 1 h con carga alta.

Si mientras tanto otra sesión aplicaba una migración a esa base, la etapa corría contra un esquema que su clave no nombraba. El verde se guardaba con la huella vieja y se habría reutilizado contra una base en la que nunca se midió.

**Patrón:** una clave de caché describe el estado en el que se mide, no el estado en el que se pidió turno.
- Recalcúlala al terminar y guarda el resultado solo si coincide con la de antes.
- Si no coincide, di qué componente cambió.

Lo mismo vale para cualquier trabajo encolado que valide algo mutable y compartido: árbol, `.env`, base, dependencias.

Relacionado: una sonda que resuelve credenciales con un tope de 30 s también se queda sin clave cuando la máquina está saturada. Falla segura (la etapa corre igual), pero la caché no ahorra nada justo cuando más falta hace. Ver [[un-trabajo-en-cola-que-guarda-el-texto-y-no-la-referencia-nace-caducando]].
