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

Barato, pre-merge, ROI alto. Misma maquinaria que [[verificacion-adversarial-lentes-triar-por-que-lente-refuta]], aplicada a tu propio diff.
