---
title: n8n parte el mensaje de error en el primer ": " y el prefijo no llega a Slack
date: 2026-08-24
source: tecnocloud, centro-elphis
tags: [n8n, observabilidad, alertas]
---

`throw new Error('MENOR: el aviso sí salió…')` en un Code node → n8n guarda
`error.description = 'MENOR'` y `error.message` = **el resto** (+ sufijo ` [line N]`). El Error
Handler típico publica `{{ …error.message }}`, así que **el prefijo desaparece del aviso**. Medido en
Tecnocloud (exec 1254, 24-ago) y en Centro Elphis (exec 11899, 4-sep).

- **No es solo cosmético.** Si el handler *clasifica* por ese prefijo (severidad, color, ventana de
  dedup, texto en castellano), buscarlo en `message` no encuentra nada y **todos los códigos caen al
  default**: rojos, sin explicación y con clave de dedup genérica, que colapsa dos casos distintos en
  un solo aviso. En Elphis fueron los 10 códigos, 8 días.
- **Patrón que funciona** (`error-handler-global`, 4-sep): comparar **por igualdad** contra dos
  candidatos —`description` limpia de ` [line N]` y el prefijo de `message` hasta el `:`— y calcular
  el detalle aparte para la clave por caso. Por igualdad y **nunca por inclusión**: un fallo de SQL
  cuya query contenga el literal se disfrazaría de flujo previsto.
- **Peor en sub-workflows** (n8n 2.20.9, medido 4-oct en Elphis): con `executeWorkflow` y
  `waitForSubWorkflow:true`, el `errorWorkflow` del sub **no se dispara** y al padre (con
  `onError: continueRegularOutput`) solo le llega `{error}` con el **último** trozo tras los `:`.
  Patrón: el sub **devuelve** el aviso como dato (`{__aviso:'codigo: detalle'}`) y el padre lo
  reenvía a un workflow que hace el `throw`.
- Alternativa si el handler es de otro: que el mensaje no lleve `": "` (usar raya, `GRAVE — …`).
- Fondo: una alerta que no distingue severidad manda a mirar donde no hay nada, y se aprende a
  ignorarla. Ver [[un-gate-cuyo-fuente-es-copia-de-lo-desplegado-caduca-y-nadie-lo-corre]].
