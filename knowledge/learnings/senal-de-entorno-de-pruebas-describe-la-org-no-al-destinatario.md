---
title: is_test describe la organización, no al destinatario — gatear por él solo apaga lo interno
date: 2026-07-31
source: claude-code-session
tags: [email, sandbox, multi-tenant, efectos-externos]
---
Al impedir que un entorno de pruebas escriba al mundo, la reacción es gatear por
`organizations.is_test` y no enviar. Medirlo lo desmiente: de los 89 emails históricos de la
organización sandbox, la mayoría eran **operativos internos** (alertas de sistema, tickets de
feedback, alarmas de stock) dirigidos al propio equipo. Bloquear por organización los apaga
justo en el entorno donde más QA se hace, que es donde más falta hacen.

`is_test` describe la ORGANIZACIÓN (sus datos son falsos); el riesgo lo define el DESTINATARIO
(la persona es real). Ninguna señal sirve sola: solo la org apaga lo interno; solo el
destinatario dejaría a una organización REAL sin escribir a sus clientes, que es romper el
producto. **La condición es la conjunción**, y conviene que un test la fije por los dos lados.

Y mejor **redirigir que bloquear**: la fila queda `sent`, el correo es inspeccionable, no hace
falta migración ni un estado nuevo que la UI no sepa pintar. Fail-open si no se puede resolver
la señal. Caso real: FacturaIA `qa-014`, PR #1418.
