---
title: un test contra producción que pasa rápido y mudo no tocó la red
date: 2026-09-01
source: facturaia
tags: [testing, verificacion, gates]
---
Para verificar algo en producción ejecutando el código real (no una fila en Postgres), lo cómodo es
un test suelto en el runner del repo, que ya trae los alias y los mocks. El riesgo es el verde
vacío: si el env no cargó, si un mock interceptó el cliente o si el runner silenció la salida, el
test pasa **sin haber medido nada** y no hay forma de distinguirlo de un pase real.

Tells (1-sep, facturaia): 185 ms para siete queries a Supabase, y el `console.log` que no aparece.

- Fix: **poner un aserto deliberadamente falso** y leer la medida en el mensaje de error —
  `expect(\`avisos=\${n} huerfanas=\${h}\`).toBe('CENTINELA')` imprime `avisos=0 huerfanas=0`. Si no
  hubiera tocado la red, no habría cifra que enseñar.
- Es el mismo principio que [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] aplicado al
  arnés en vez de al código: el caso que DEBE fallar es el único que discrimina.
- Un `console.log` no sirve de prueba: el runner puede tragárselo. El mensaje de un aserto, no.
