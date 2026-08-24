---
title: n8n parte el mensaje de error en el primer ": " y el prefijo no llega a Slack
date: 2026-08-24
source: tecnocloud
tags: [n8n, observabilidad, alertas]
---

`throw new Error('MENOR: el aviso sí salió…')` en un Code node → n8n guarda
`error.description = 'MENOR'` y `error.message` = **el resto**. El Error Handler típico publica
`{{ $json.execution.error.message }}`, así que **la severidad desaparece del aviso de Slack** aunque
esté en el código. Medido en Tecnocloud (exec 1254, 24-ago).

- Si el prefijo tiene que llegar, que **no haya ningún `": "` en el mensaje**: usar raya (`GRAVE — …`).
  Ojo a los dos puntos que aparecen a media frase, no solo al principio.
- Alternativa: tocar el Error Handler para publicar también `description`. Peor idea si ese handler es
  compartido por varios workflows del cliente.
- Y el fondo del asunto: la alerta llevaba meses diciendo «revisar si soporte se ha quedado sin el
  aviso» cuando el email había salido bien y solo había fallado la hoja de registro. Una alerta que no
  distingue severidad manda a mirar donde no hay nada, y se aprende a ignorarla.
