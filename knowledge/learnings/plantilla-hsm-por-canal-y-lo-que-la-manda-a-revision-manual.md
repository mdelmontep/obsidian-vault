---
title: una plantilla de WhatsApp por canal, y el emoji que la deja 16 h en revisión
date: 2026-08-18
source: claude-code-session
tags: [whatsapp, meta, hsm, plantillas, notificaciones, elphis]
---
El aviso interno de leads usaba UNA plantilla para voz y chat, con texto fijo «…a través del bot de
WhatsApp… revísalo en Chatwoot». Un lead que había **llamado** llegaba con ese texto y la persona se
puso a buscar en Chatwoot una conversación que no existía.

- El texto fijo no puede depender del canal: **una plantilla por canal**. Lo variable ya cabe en los
  parámetros, pero la frase «dónde seguir» es fija y es justo la que cambia.
- **No lo digas en negativo.** «No hay chat en Chatwoot» se lee como que algo se ha perdido; la de voz
  termina en «Ficha completa en Clientify» y punto.
- **Qué manda una plantilla a revisión manual**: la versión con **emoji inicial** y la palabra
  **«grabación»** llevaba 16 h en `PENDING`; su gemela sin las dos cosas, creada después, se aprobó
  en minutos. Manda las dos variantes a la vez y usa la que apruebe.
- **No se recrea con el mismo nombre**: borrar y volver a crear con nombre+idioma iguales da
  `2388023` («se está eliminando el idioma») durante un buen rato. Nombre nuevo.
- Los **parámetros** no admiten saltos de línea, tabuladores ni 4+ espacios seguidos (1024 chars máx):
  si uno lo escribe un LLM, aplánalo con `replace(/\s+/g,' ')` antes de enviar.
- Nunca cambies el código a una plantilla `PENDING`: el aviso de leads se cae entero hasta que aprueben.
