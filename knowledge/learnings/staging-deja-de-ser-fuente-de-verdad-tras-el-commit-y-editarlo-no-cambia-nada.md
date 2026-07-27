---
title: un staging deja de ser fuente de verdad tras el commit, y editarlo sigue "guardando"
date: 2026-07-27
source: claude-code-session
tags: [arquitectura, datos, ux, integridad]
---

Patrón: un buffer de staging (JSONB de OCR, borrador, carrito, fila de import) se copia
al registro real **en el commit de estado** (aprobar / publicar / confirmar). A partir de
ahí el registro manda y el staging es solo el acta de lo que se leyó.

La trampa: la pantalla del staging sigue viva y editable. El usuario corrige un campo
después de aprobar, la escritura persiste **en el staging** con éxito y el registro no
cambia. Nadie ve un error. Caso real FacturaIA (ticket 72f0545c, cliente IET): fecha de
vencimiento que el OCR no cogió; el usuario la escribió tres veces y la factura seguía sin
ella. Además NO había otra vía: el editor del registro estaba gateado al estado previo.

Reglas:
- Tras el commit, la pantalla del staging muestra el valor **del registro**, no el del buffer.
- Lo que ya no se puede cambiar se **bloquea con el motivo** (un campo editable que no
  persiste es peor que uno bloqueado) y lo demás se rechaza en voz alta desde el ÚNICO
  punto por el que pasan las escrituras, no campo a campo.
- Si un dato sigue siendo corregible después (no es fiscal/inmutable), dale endpoint propio
  y ponlo también en el registro, no solo en el staging.

Ver [[editor-inline-que-compara-contra-el-valor-mostrado-encalla-al-reescribir-lo-mismo]] ·
[[form-parcial-upsert-fila-completa-borra-columnas-no-enviadas]]
