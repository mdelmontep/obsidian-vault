---
title: el log de auditoría de la plataforma dueña dice de qué lado ocurrió el cambio
date: 2026-09-11
source: laserys-las-rozas
tags: [integraciones, debug, meta, kommo]
---
Dos paneles discrepan sobre un estado (el SaaS dice desconectado, la plataforma dueña del activo
dice conectado) y la discusión se vuelve «nosotros no fuimos» contra «pues yo no toqué nada».
Lo zanja el **registro de auditoría de quien es dueño del activo**: si el evento no está ahí, el
cambio no pasó por esa plataforma y es interno del SaaS. Sirve como prueba en un ticket, sin acceso
a su backend.

Caso Laserys (11-sep): el canal de Kommo dejó de mostrar el número de un día para otro. El
*Registro de actividad* de la WABA en Meta no tenía **ninguna** entrada de ese día — la última era
la instalación de la app de Kommo la tarde anterior. Con eso, la desvinculación queda ubicada
dentro de Kommo y deja de ser opinable.

Mirar también si el log recoge **tu propia** acción: su ausencia delata que el OAuth que creías
haber rehecho no llegó a la plataforma.

Ver [[un-id-que-ensena-un-saas-hay-que-resolverlo-contra-la-plataforma-que-lo-emite]].
