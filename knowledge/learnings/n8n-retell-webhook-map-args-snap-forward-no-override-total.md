---
title: n8n retell webhook map-args debe usar fechas del llm con snap-forward, no ignorarlas
date: 2026-06-04
source: claude-code-session
tags: [n8n, retell, fechas, webhook]
---
Patrón incorrecto: `Map args` hardcodeaba `from_iso = now+24h, to_iso = now+14d` ignorando los
parámetros del LLM → el agente siempre consultaba los mismos días sin importar lo que pedía el usuario.
Patrón correcto: usar `from_iso`/`to_iso` del LLM + snap-forward si son pasadas:
```js
if (!fromDt || toDt <= earliest) { // ventana pasada → fallback 8 días
  fromDt = earliest; toDt = fromDt.plus({days:8});
} else if (fromDt < earliest) {   // solo from pasado → snap manteniendo ancho
  const w = toDt - fromDt; fromDt = earliest; toDt = fromDt.plus({ms:w});
}
```
