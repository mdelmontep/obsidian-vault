---
title: no dejar que el LLM sobrescriba un dato que el canal de origen ya conoce con certeza
date: 2026-08-12
source: claude-code-session
tags: [n8n, llm, retell, patron]
---
Un chatbot de WhatsApp sabe el teléfono real del cliente con certeza absoluta — es el canal por el
que llegó el mensaje, Kommo/Meta ya lo tienen guardado bien. Pese a eso, el flujo dejaba que el LLM
extrajera `numero_de_telefono` del TEXTO de la conversación (`$fromAI(...)`) y usaba ese valor para
hacer un UPDATE que SOBREESCRIBÍA el campo teléfono ya correcto del contacto — así que un cliente que
nunca dictó su número completo (no hacía falta, ya se sabía) terminaba con el campo real pisado por
lo que el LLM "creyó" extraer (en un caso real: literalmente `"+34"`, sin dígitos detrás). Reventó
más tarde al intentar enviar la confirmación por WhatsApp: "phone number is malformed".

Fix: antes de escribir el dato, leer el valor ACTUAL en el sistema (GET del contacto) y usarlo como
fuente de verdad — el dato del LLM solo se usa como fallback si el actual no existe o es inválido,
nunca al revés. Regla general: si el canal/sistema de origen YA conoce un dato con certeza, un LLM
nunca debería tener autoridad para pisarlo — solo para rellenarlo cuando falta.

Relacionado pero distinto de [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]] (ese resuelve
referencias ambiguas antes del LLM; este evita que el LLM sobrescriba un dato ya certero).
