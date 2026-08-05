---
title: una rpc de borrado que enumera hijos a mano se rompe con cada tabla nueva; el arreglo es un guard estático
date: 2026-08-06
source: claude-code-session
tags: [postgres, bd, fk, testing, guard]
---

Si borrar una entidad pasa por una RPC que va desenganchando hijos uno a uno,
esa lista caduca sola: cada módulo nuevo cuelga su tabla con `ON DELETE RESTRICT`
(correcto para un justificante) y nadie se acuerda de tocar la RPC. El borrado
revienta con un `23503` que la API traduce a un error genérico.

- Caso TuFacturaIA (mig 640): `factura_pagos` nació con RESTRICT y
  `recibida_eliminar` no la conocía → una recibida marcada pagada dejaba de
  poderse borrar, rompiendo el inviolable de que una recibida se borra en
  cualquier estado. Lo mismo había pasado antes con `merge_cliente` (mig 599).
- Arreglo real: **guard estático** que escanea las migraciones, saca las tablas
  con FK bloqueante al padre y exige que aparezcan en el cuerpo de la última
  definición de la RPC. Con ALLOWLIST razonada para las excepciones.
- Al escribirlo, dos trampas: (1) acumula la sentencia hasta `,`/`;`, **nunca
  cortes en el `)`** — el `ON DELETE` va en la línea siguiente y salen falsos
  positivos de FKs que sí eran CASCADE; (2) un guard con falsos positivos se
  arregla en el DETECTOR, no tapándolos con allowlist, o deja de creerse.
- Verifica que discrimina: quita la línea del DELETE y el test debe ponerse rojo
  nombrando la tabla. Verde en ambos sentidos no prueba nada.

Ver [[bandeja-staging-tabla-real-fk-restrict-borrar-sincroniza-ambos-lados]] ·
[[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]]
