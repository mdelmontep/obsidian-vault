---
title: variables de plantilla whatsapp no admiten saltos de linea ni tabs (#132018)
date: 2026-06-02
source: claude-code-session
tags: [whatsapp, meta, kommo, plantillas]
---
Una variable {{N}} de plantilla WhatsApp NO puede contener \n, tab ni >4 espacios seguidos.
Meta rechaza el envío con error #132018 "Param text cannot have new-line/tab characters
or more than 4 consecutive spaces".
Trampa: el salesbot/run de Kommo devuelve 200 (lanza el bot); el rechazo de Meta es ASÍNCRONO
→ la ejecución parece OK pero el mensaje no llega nunca.
Fix: texto dinámico multi-item en UNA sola línea (separadores tipo " — "), sin saltos.
Si necesitas formato bonito/varias líneas → mandarlo como texto libre dentro de la ventana 24h
(p.ej. el chatbot al responder), no en variable de plantilla.
Ver [[kommo-custom-field-rechaza-emoji-4-byte]] · [[kommo-salesbot-run-success-sin-acciones]].
