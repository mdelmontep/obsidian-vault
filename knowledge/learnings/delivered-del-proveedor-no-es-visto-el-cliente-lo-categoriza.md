---
title: "delivered" del proveedor no es "visto" — el cliente de correo lo categoriza
date: 2026-08-03
source: claude-code-session
tags: [email, entregabilidad, resend, diagnostico, facturaia]
---
`delivered` de Resend/SES solo dice que el **MX destino aceptó** el mensaje (250). Lo que
pase dentro del buzón —spam, pestaña, categoría, regla— no vuelve al emisor: no hay evento,
no hay rebote, y el log del emisor se queda en verde para siempre.

Caso real (TuFacturaIA, 03-ago): «no me llegan los avisos de ticket». Todo el flujo estaba
bien —36 avisos `delivered`, DKIM `resend._domainkey`, SPF de `send.tufacturaia.com`, DMARC—
y el correo estaba **en la Entrada**. Dos trampas del Mail de macOS lo escondían:
- La **bandeja categorizada**: la Entrada se ve filtrada por «Principal» y los transaccionales
  caen en otra categoría, así que lo más nuevo que ves es de una hora antes. Fix: clic derecho
  → Categorizar remitente → Principal.
- **«Archivado» sobre Gmail/IMAP es «Todos los mensajes»**, no un archivo: enseña también lo
  que sigue en la Entrada. La carpeta real la dice la etiqueta del mensaje abierto.

Antes de tocar SPF/DKIM/DMARC o la configuración del emisor, pide una **captura del buzón**
con la carpeta y la categoría a la vista. El reverso de esto —aceptado pero nunca entregado—
en [[smtp-acepta-con-250-queued-y-no-entrega-fuera]]. Ver [[facturaia]]
