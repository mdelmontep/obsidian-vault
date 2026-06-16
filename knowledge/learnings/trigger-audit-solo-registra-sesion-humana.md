---
title: trigger de auditoría por auth.uid() no registra acciones service-role
date: 2026-06-16
source: claude-code-session
tags: [supabase, postgres, auditoria, trigger, service-role]
---

Un trigger SQL de auditoría que atribuye autor vía `auth.uid()` (o lo exige no-null)
**se salta los cambios sin sesión de usuario**: service-role (copiloto, crons, jobs,
admin client). Si una UI muestra "historial" leyendo SOLO lo que escribe ese trigger,
las acciones automáticas quedan **invisibles** (parecen no haber pasado).

Fix: el código que actúa con service-role debe escribir su **propia** fila de audit
explícita, con la `entidad`/`accion` que la UI reconoce — no confiar en el trigger.

Gotcha doble (caso TuFacturaIA, cobro por Copiloto no salía en la ficha):
- La `entidad` debe coincidir EXACTA con el filtro de la UI: `'facturas'` (plural),
  no `'factura'`. Un singular/plural distinto = fila escrita pero nunca leída.
- Da igual el `actor_type`: si la UI mapea `accion`→etiqueta, añade la accion al MAP
  o saldrá el string crudo.

Relacionado: [[consumidor-lee-claves-que-productor-no-emite]] (mismo origen: el
consumidor espera una forma/columna que el productor nunca emitió).
