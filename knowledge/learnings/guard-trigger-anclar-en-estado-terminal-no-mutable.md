---
title: un guard/trigger de inalterabilidad debe anclarse en estado terminal, no en uno mutable
date: 2026-06-23
source: claude-code-session
tags: [seguridad, postgres, trigger, fiscal]
---
Un trigger que congela campos "protegidos" condicionando el freeze a un campo que el MISMO actor puede mutar es **bypassable en 2 pasos**: UPDATE-1 degrada el campo-condición (contenido intacto → permitido), UPDATE-2 edita lo "protegido" (ya no se cumple la condición).

Fix: anclar el freeze en un estado **TERMINAL/inmutable** y, además, **bloquear la regresión de ese estado** dentro del propio trigger.

Caso: mig 376 verifactu (facturas). Primer diseño congelaba contenido si `verifactu_estado <> 'no_aplica'` → bypass degradando estado a `pendiente_envio`. Fix: anclar en `aceptada`/`aceptada_con_errores` (terminal: el worker nunca sale de ahí) + bloquear que `NEW.verifactu_estado` salga del conjunto aceptado.

Bonus: elegir bien el ancla terminal evita falsos positivos — `pendiente_envio` lo asigna el INSERT trigger también a borradores → congelar ahí rompería editarlos. Recuerda: los triggers SÍ corren bajo `service_role` (RLS no) → son la barrera real contra SQL directo. Ver [[columnas-regulatorias-requieren-guard-rol-trigger-no-solo-rls]].
