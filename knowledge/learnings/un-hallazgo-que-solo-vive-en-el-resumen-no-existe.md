---
title: un hallazgo urgente que solo vive en el resumen del chat no existe
date: 2026-08-09
source: claude-code-session
tags: [metodo, documentacion, planificacion]
---
Tras integrar ocho documentos de diseño en un plan, di cuatro puntos como «lo urgente». Al preguntarme el
usuario «¿pero está en el plan?», la comprobación fue incómoda: **uno de los cuatro estaba bien anclado**.
Los otros tres vivían en un documento de sección o en mi propio mensaje.

El criterio que faltaba no es «¿está escrito?», es **«¿está donde va a mirar quien lo construya?»**:
- Una restricción de la épica B se escribe **en la épica A** si A es la que se abre primero (el orden entre
  las dos es la restricción).
- Un incumplimiento se anota **en la épica que figura cerrada**, no en un anexo de deudas.
- El trabajo que hay que hacer en **otro repositorio** se lista en el plan de éste, porque es justo el que
  se evapora.

Vale para planes, para ADRs y para issues: escribir el hallazgo en el punto de entrada de quien lo va a
tropezar, no en el resumen de quien lo encontró.
