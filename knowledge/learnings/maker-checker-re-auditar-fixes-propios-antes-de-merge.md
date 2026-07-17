---
title: maker/checker — re-audita tus propios fixes con agentes independientes antes de mergear
date: 2026-07-07
source: AGH re-auditoría Tier 1 agente Carlos
tags: [meta, audit, multi-agent, review]
---
El que hizo el fix no es buen juez. Tras cerrar una tanda de fixes, pásalos por una re-auditoría
adversarial INDEPENDIENTE (agentes + fuentes oficiales OWASP/docs) ANTES de mergear. En AGH cazó, en mi
propio trabajo:
- un bug CRÍTICO que el fix introdujo: el fix de seguridad (auth del WS Retell) LOGUEABA el secreto que
  protege — `console.log(req.url)` con el secreto ya en el path, en el 100% de llamadas legítimas.
- una regresión: tokenizar solo por espacios rompía «E-commerce»/«CI/CD».
- un half-fix con `Closes` que habría cerrado un issue a medias → si arreglas solo una parte usa `Refs #N`
  y deja el issue abierto (no auto-cierres el tracker del residual).

Reforzado 2026-07-17 (módulo Obras, 3 cierres /fia-cierre seguidos): cada tanda de fixes metió un aviso
nuevo que solo cazó la auditoría SIGUIENTE — ping-pong de a11y (el "fix a11y" dejó la fila sin teclado),
CTA de notificación a ruta 404, y el bug fecha-vs-timestamp repetido en 2 sitios. El gate (lint/tc/build)
NO ve rutas rotas, a11y ni formato → re-auditar el DIFF DE LOS ARREGLOS (code-review + QA visual), no
solo confiar en el gate verde.

Barato, pre-merge, ROI alto. Misma maquinaria que [[verificacion-adversarial-lentes-triar-por-que-lente-refuta]], aplicada a tu propio diff.
