---
title: quitar un scope de google oauth no lo retira a quien ya lo concedió (include_granted_scopes)
date: 2026-10-13
source: facturaia (#3386, gmail.send fuera de GOOGLE_SCOPES)
tags: [google, oauth, scopes, integraciones]
---
Sacar un scope de la lista que pide `generateAuthUrl` solo cambia las conexiones NUEVAS. Con `include_granted_scopes: true` (autorización incremental), el token de una cuenta que ya lo concedió sigue cubriéndolo aunque reconecte con `prompt: 'consent'`.

Caso real: #3386 retiró `gmail.send` y el manual decía «se retira al reconectar». Era falso; lo cazó el /fia-cierre.

Para retirarlo de verdad: quitar `include_granted_scopes`, revocar el token (`oauth2.googleapis.com/revoke`) y que reconecte, o que el usuario quite el acceso en su cuenta de Google. Al documentar una retirada de permisos, decir a qué conexiones aplica.
