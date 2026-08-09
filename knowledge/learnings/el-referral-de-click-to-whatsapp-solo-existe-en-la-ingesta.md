---
title: el referral de click-to-whatsapp solo existe en la ingesta y no se recupera después
date: 2026-08-09
source: claude-code-session
tags: [whatsapp, meta, atribucion, marketing]
---
Un mensaje que llega desde un anuncio de Click-to-WhatsApp trae en el webhook un bloque `referral` con
`ctwa_clid`, `source_id`, `source_url` y el titular del anuncio. Es **lo único** que dice de qué campaña
vino ese cliente.

Dos trampas juntas:
- **`wa.me` no transporta origen.** El único portador desde una web es el texto prellenado, así que un
  botón de WhatsApp tiene que acuñar su propio código antes de abrir el chat.
- **El `referral` no se puede pedir después.** No está en la API, y la tabla de eventos crudos se redacta
  y se purga por diseño (RGPD). Si no se persiste en la MISMA transacción que guarda el mensaje entrante,
  se pierde para siempre y ninguna atribución ni Conversions API lo puede reconstruir.

Regla: en cualquier integración de WhatsApp, `persistReferral()` va dentro de la ingesta, nunca en una
fase posterior del plan. Es de las pocas decisiones de calendario que son irreversibles.
