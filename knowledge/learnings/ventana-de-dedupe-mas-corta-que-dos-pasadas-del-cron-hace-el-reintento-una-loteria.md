---
title: una ventana de dedupe más corta que dos pasadas del cron hace el reintento una lotería
date: 2026-09-10
source: laserys-las-rozas
tags: [n8n, cron, idempotencia, recordatorios, whatsapp]
---

Dos fallos que viajan juntos en todo scanner con marca de "ya enviado":

1. **Marcar antes del efecto.** `staticData.enviados[clave] = Date.now()` estaba en el nodo que
   filtra, antes del envío: un WhatsApp fallido quedaba por entregado y nadie lo reintentaba. La
   marca va DESPUÉS, en un nodo que lea `$json.error` (`onError: continueRegularOutput` +
   `alwaysOutputData`) y solo marque lo que salió bien; lo fallido sigue vivo y avisa.

2. **La ventana tiene que cubrir dos pasadas.** Marcar después solo sirve si el ítem vuelve a
   entrar. Con cron cada 30 min y ventana de ±20 (40 de ancho) hay una pasada garantizada y una
   segunda solo el 33 % de las veces: el reintento era suerte. Regla: `ancho > 2 × periodo` —
   ±35 min (70 de ancho) da dos pasadas siempre.

Verificado en un workflow espejo con lote mixto: pasada 1 falla y no marca · pasada 2 el mismo ítem
reentra, sale bien y se marca · pasada 3 ya no se reenvía. Ver
[[un-nodo-de-log-con-onerror-continue-puede-no-haber-escrito-nunca]] ·
[[un-discriminador-en-memoria-no-sobrevive-a-la-pasada-siguiente]].
