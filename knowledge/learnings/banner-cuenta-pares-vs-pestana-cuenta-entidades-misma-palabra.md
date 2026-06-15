---
title: dos contadores con la misma palabra pero distinta unidad confunden — cuenta la entidad del usuario, no las filas del join
date: 2026-06-15
source: claude-code-session
tags: [ux, conciliacion, facturaia, frontend]
---

Síntoma real: el usuario ve "5 sugerencias" en un banner y "Con sugerencia 1" en la pestaña, en la misma pantalla, y no entiende nada.

Causa: medían cosas distintas con la misma palabra. El banner contaba **filas del join** (pares factura↔movimiento, N facturas candidatas por movimiento → 5 filas). La pestaña contaba **movimientos distintos** (la entidad que el usuario manipula → 1). Ambos correctos, juntos ilegibles.

Regla: en contadores de cara al usuario, **cuenta la entidad que el usuario acciona** (el movimiento/la factura), no las filas internas. Si necesitas mostrar las dos magnitudes, hazlas explícitas: *"1 movimiento con coincidencias · 5 posibles"*, nunca dos "5"/"1" sueltos con la misma etiqueta.

Aplica a cualquier lista con banner-resumen + filtro-pestaña sobre el mismo dataset (sugerencias, alertas, duplicados). Verifica que banner y filtro usan la MISMA unidad. Relacionado: [[auditar-un-lado-de-par-simetrico-revisar-el-espejo]].
