---
title: traefik.me no emite certificado — el cupo de let's encrypt es por dominio registrado
date: 2026-08-02
source: claude-code-session
tags: [dokploy, tls, dns]
---
Los dominios comodín públicos (`traefik.me`, `sslip.io`) resuelven a cualquier IP y van bien para exponer
algo sin tocar DNS, pero **Let's Encrypt cuenta su cupo por dominio registrado, no por subdominio**: como
lo comparten miles de usuarios, suele estar agotado y el certificado nunca se emite. Traefik sirve el
autofirmado y el navegador falla, sin error propio en el panel.

No es fallo del servidor ni de la configuración. Se resuelve con dominio propio. Mientras tanto, HTTP
explícito y **sin datos reales de clientes**.
