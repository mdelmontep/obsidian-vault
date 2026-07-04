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
  `auditoria-section.tsx` sí tiene `ENTIDAD_LABEL` (mapa entidad→español, con
  fallback al string crudo) — añadir ahí cualquier entidad nueva.
- `accion` NO tiene mapa de humanización (a diferencia de `entidad`): se
  renderiza LITERAL en la UI. Escribe la frase en español ya en el `logAgentAction`
  ("Movimiento bancario eliminado"), nunca claves máquina tipo `entidad.verbo`
  — ese estilo solo es correcto para `actor:'agent:api'` (precedente:
  `factura.anular`), no para `actor:'human'`. Recurrencia 2026-07-04: 27 `accion`
  de un PR grande (auditoría de conciliación) salieron en formato máquina para
  actor human; solo se detectó con smoke visual real de la pantalla, no
  verificando inserts en BD.

Relacionado: [[consumidor-lee-claves-que-productor-no-emite]] (mismo origen: el
consumidor espera una forma/columna que el productor nunca emitió).
