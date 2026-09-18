---
title: kommo acorta los enlaces que manda el salesbot, pero no los de dentro de una plantilla waba
date: 2026-09-18
source: clinica-zen
tags: [kommo, whatsapp, enlaces, salesbot]
---

Todo enlace dentro de un mensaje de TEXTO lanzado por salesbot sale reescrito como
`https://kommo.cc/K/XXXX` (y genera evento `link_followed` en el contacto). El destino funciona, pero
el paciente ve un dominio de Kommo, no el tuyo ni el de Google. No hay opción para desactivarlo en el
canal WhatsApp nativo: la que documenta Wazzup («descifrar los enlaces del Salesbot») es de SU
integración, no de Kommo.

Lo que NO reescribe: los enlaces dentro de una **plantilla WABA** —ni en el cuerpo ni en un botón
`type: url`—. Verificado el 15-sep-2026 en Clínica Zen: el recordatorio con `maps.app.goo.gl` sale
intacto, y el mismo enlace en un texto del bot sale como `kommo.cc`.

Fix si el enlace tiene que verse limpio (reseña de Google, pago, formulario): plantilla aprobada con
botón URL en vez de texto del bot. Quitar el `https://` NO sirve: WhatsApp lo deja en texto plano.
