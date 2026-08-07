---
title: una fila basura amplifica el error de redondeo de toda la tabla
date: 2026-08-07
source: claude-code-session
tags: [numeric, redondeo, migraciones, datos]
---

Al reescalar precios, `NUMERIC(12,4)` parecía sobrado: `33 × 1,421135 =
46,897455` se guardaba como `46,8975`, un error de 45 millonésimas de euro por
hora. Invisible en cualquier fila normal.

Pero el catálogo tenía una partida con `tiempo_mo_horas = 1000` — que no son
horas, son EUROS metidos por la columna de tiempo («VARIOS PARA OFERTAS DE 10000
EUROS»). Esas 45 millonésimas × 703 horas = **3 céntimos**, y el assert abortó
la migración: 66.250,00 → 66.250,03.

**La regla**: la precisión que necesita una columna no la marca el valor típico,
la marca el valor MÁXIMO. Antes de elegir la escala, `SELECT max(col)` y calcula
el error ahí. Y si el factor tiene N decimales, el producto necesita al menos N.

**El corolario incómodo**: las filas basura que documentas y decides ignorar
siguen participando en los cálculos. «Ya sé que esa fila es rara» no la excluye
de nada — solo te hace no mirarla cuando falla.

Relacionado: [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]] ·
[[un-trigger-que-pisa-en-vez-de-calcular-resincroniza-al-migrar]]
