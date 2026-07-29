---
title: agent-browser aborta el clic si un aviso flotante lo tapa — quítalo con eval, no busques otro selector
date: 2026-07-29
source: claude-code-session
tags: [agent-browser, smoke, facturaia]
---

`agent-browser click` no clica a ciegas: comprueba qué elemento hay en el punto de impacto y
aborta con "is covered by <X> at its click point". Es lo correcto (evita clics fantasma), pero
el mensaje invita a buscar otro selector cuando el problema es el elemento que estorba.

Caso TuFacturaIA: en `/admin/feedback`, el globo pulsante de avisos del admin
(`.adm-alertbub-ping`, banner de tickets nuevos y respuestas sin leer) se solapa con la columna
de botones "Ver" de la tabla. Ningún selector alternativo lo arregla: hay que retirar el
estorbo.

```
agent-browser eval "document.querySelectorAll('[class*=alertbub]').forEach(e=>e.remove()); 'ok'"
```

Ojo: el `eval` se pierde en cada `open`/recarga — repetirlo justo antes del clic, no una vez al
principio. Y si el aviso es lo que estás verificando, entonces el estorbo ES el hallazgo:
mídelo antes de borrarlo.

Ver [[agent-browser-verificar-snapshot-no-solo-screenshot]] ·
[[clic-por-coordenadas-tras-salto-de-layout-no-cae-en-el-boton]]
