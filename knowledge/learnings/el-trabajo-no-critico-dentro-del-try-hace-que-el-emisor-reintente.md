---
title: el trabajo no crítico dentro del try del crítico hace que el emisor reintente
date: 2026-08-27
source: agency-portal
tags: [webhooks, idempotencia, robustez, api]
---
Un receptor de webhook hacía, dentro de UN solo `try`: (1) escribir el log de idempotencia,
(2) el trabajo crítico —sincronizar el documento—, (3) una lectura extra para **enriquecer la
auditoría** (a qué cliente pertenece). Su `catch` trata cualquier error como transitorio: BORRA el
log de idempotencia y devuelve 500 para que el emisor reintente. Correcto para (1) y (2); veneno
para (3): un fallo de la lectura cosmética deshacía la marca de un documento **ya sincronizado** y
FacturaIA volvía a mandarlo. El síntoma no es un error, es un reintento eterno de algo que fue bien.

Regla: **en cuanto el trabajo crítico ha terminado bien, todo lo que venga después va en su propio
`try/catch`** — enriquecimiento, auditoría, notificaciones, métricas. Si no, el `catch`
compensatorio del bloque crítico los trata como si hubiera fallado lo crítico. Prueba que lo
discrimina: forzar el fallo SOLO del paso posterior y exigir **200** y que el log siga escrito, con
el campo enriquecido a `undefined`. Hermano de [[columna-de-purga-sin-cron-es-retencion-aparente]]:
la compensación tiene que cubrir exactamente lo que compensa, ni un paso más.
