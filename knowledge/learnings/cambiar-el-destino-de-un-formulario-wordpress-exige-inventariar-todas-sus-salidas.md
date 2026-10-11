---
title: cambiar el destino de un formulario wordpress exige inventariar todas sus salidas
date: 2026-10-05
source: centro-elphis (formulario «Te llamamos», Clientify → Holded)
tags: [wordpress, contact-form-7, crm, formularios]
---
Un formulario de Contact Form 7 rara vez tiene una sola salida. En Centro Elphis el «Te llamamos» tenía cuatro, y en tres pestañas distintas del editor:
- el **correo** de CF7;
- el **webhook** (plugin CF7 to Webhook, antes apuntaba a Zapier);
- **FormsCRM**, que seguía empujando a Clientify con su propia API password;
- y el **popup** que lo muestra, que en realidad incrustaba un superform de Clientify, no el CF7.

Si solo cambias el webhook, el CRM viejo sigue recibiendo leads sin que nadie los mire.

Patrón:
1. Abrir el popup o la página y ver qué se sirve de verdad (DOM, iframe, script de terceros).
2. Recorrer TODAS las pestañas del formulario y apuntar cada salida antes de tocar nada.
3. Apagar las salidas viejas en origen. FormsCRM no tiene opción «ninguno», así que se vacía la clave.

Gotchas:
- En CF7 to Webhook, «Send CF7 mail as usually» desmarcado **omite el correo**: déjalo marcado.
- Si el tema pisa los estilos con `form input:not(...)`, el CSS réplica necesita `!important`.
- Un envío de prueba manda el correo real del cliente: avísale.
