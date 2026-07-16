---
title: imapflow (SSRF-safe) — pinear por IP exige servername explícito + doSTARTTLS explícito
date: 2026-07-17
source: claude-code-session
tags: [ssrf, imap, imapflow, security, tls, dns-rebinding]
---

Al validar un destino IMAP elegido por el usuario (defensa SSRF: resolver DNS,
rechazar IPs privadas) y luego CONECTAR contra la IP ya validada (pinning
anti DNS-rebinding, no re-resolver el hostname), imapflow tiene dos trampas
verificadas en su código fuente (`imap-flow.js`):

1. **`servername` no se infiere solo**: si pasas `host` como IP literal sin
   fijar `servername` explícito, imapflow deriva `servername = false` (línea
   ~282: `!net.isIP(host) ? host : false`) → rompe SNI y la verificación de
   certificado TLS. Hay que pasar SIEMPRE `servername: <hostname original>`
   cuando `host` es la IP pineada — el patrón es idéntico al pinning de
   undici (`lookup` custom) pero con nombres de opción distintos.
2. **`doSTARTTLS` sin fijar = downgrade silencioso**: con `secure:false` y
   `doSTARTTLS` no definido, el modo por defecto es "oportunista" — si el
   servidor no soporta STARTTLS, la librería sigue en texto plano sin avisar
   (comentario propio de la lib: "may expose to a downgrade attack"). Hay
   que fijar `doSTARTTLS: true` explícito para el puerto no-TLS-implícito;
   así, sin soporte STARTTLS, lanza error (`tlsFailed`) en vez de continuar.

Reutilizable en cualquier protocolo TCP no-HTTP donde se valide destino de
usuario y se conecte por librería con opciones de bajo nivel (SMTP, POP3,
FTP...): comprobar SIEMPRE en el código fuente real de la librería cómo
interactúan `host`/`servername`/flags de TLS antes de asumir que "pasar la
IP" basta.
