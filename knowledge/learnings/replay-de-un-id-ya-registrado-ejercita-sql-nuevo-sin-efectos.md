---
title: replay de un id ya registrado ejercita SQL nuevo en prod sin disparar sus efectos
date: 2026-08-24
source: tecnocloud
tags: [n8n, testing, produccion, postgres]
---

Cambio en el nodo Postgres de un workflow que, más adelante en la cadena, manda un email a soporte.
No hay staging y el SQL nuevo (CTE + `ALTER TABLE … IF NOT EXISTS`) podía romper **todos** los
registros si no parseaba.

Truco: reenviar al webhook un `call_id` **ya registrado**. El `INSERT … ON CONFLICT DO NOTHING`
devuelve `duplicada`, el `IF` de idempotencia corta la rama **antes** del email y de la hoja → el SQL
nuevo se ejecuta de verdad contra el Postgres real con **cero efectos hacia fuera** (81 ms).

- Sirve para: sintaxis, columnas nuevas, permisos, que el nodo no explote.
- **No** cubre las ramas que solo existen cuando la fila es nueva — ahí ya hay que aceptar el efecto
  (y avisar de qué hay que limpiar después).
- Requisito: que la rama de idempotencia esté ANTES de los efectos. Si el email va primero, esto no
  vale.

Es el complemento de [[el-replay-que-arranca-mas-limpio-que-produccion-es-ciego]]: allí el problema es
un replay demasiado limpio; aquí se usa a propósito la rama que no hace nada.
