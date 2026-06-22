---
title: daily briefing
date: 2026-06-22
tags: [home, briefing]
---

# 🌅 Briefing 22-jun

## ✅ Lo que cerraste ayer

**Fix al parpadeo en la lista de facturas emitidas**

Resolviste un bug molesto en `/emitidas`: la pantalla parpadeaba o se volvía a renderizar sola al cambiar filtros. La raíz era que el objeto de configuración del hook se creaba de nuevo en cada render — React lo interpretaba como un cambio de datos y relanzaba la carga aunque no había nada nuevo. Con un `useMemo` la referencia queda estable y el listado solo reacciona cuando de verdad cambia algo.

**Cómo lo usas en la práctica**:
- Cuando cambias el filtro de "pendiente" a "cobrada" en `/emitidas`, la lista se actualiza limpia, sin vibración ni doble carga.
- Al revisar el estado de cobros de varios clientes seguidos, navegar entre filtros ya no interrumpe la concentración.

Ayer fue sesión corta — ese fix fue la única entrada registrada.

## 🎯 Hoy en orden de prioridad

1. **Notifs fiscal residuales (TuFacturaIA)** — Marcar como leídas las notifs viejas + abrir y recalcular los borradores 130 del 2T/3T/4T + revisar visualmente el drawer (X de 28px, fade de los chips). Trabajo manual, ~30 min.
2. **Centro Elphis — go-live** — El único bloqueo sigue siendo el host IMAP de `info@centroelphis.com`. Sin eso el flow de citas no puede arrancar. Insistir hoy a Pablo/Alba o el go-live se sigue aplazando.
3. **agency-portal — smoke PR #72** — Tras merge: verificar que el botón Sincronizar puebla campos del cliente (descripción, teléfono, web…), que el `.md` incluye la transcripción completa de WhatsApp, y que el bot pregunta por dominio/colores cuando se menciona web.

## ⏳ Pendientes y bloqueos

- **Esperando a Pablo/Alba (Elphis)**: host IMAP + contraseña `info@centroelphis.com` (bloqueado varios días)
- **Acción Manu — GitHub Actions billing**: CI muerto desde el 17/06. Arreglar pago en Settings → Billing org `AgentesIA-MAdrid`.
- **Acción Manu — OpenAI Tier 2**: bot WhatsApp salta el rate-limit (30k TPM). Subir en platform.openai.com → settings → limits.

## 💡 Quick win sugerido

**Corregir el ID del receptor en la tabla de routing de `CLAUDE.md`** — Una sola línea: `zYcHHa8jWXB6dY5i` → `pqSWkDIHqmSVHotB`. Sin esto cualquier agente nuevo que lea el CLAUDE.md acaba llamando a un workflow inexistente (404). Literalmente 1 minuto.

## ⚠️ Stale (>7 días)

- **Ticket bgchivite `1762f07e`**: el fix lleva semanas en prod, solo queda responder. 5 min o cerrar.
- **agency-portal smoke PR #67**: mergeado el 18 de mayo — más de un mes en NOW sin verificar. Hacerlo esta semana o moverlo a LATER.

---
> ⚠️ **Nota de entrega**: ntfy.sh bloqueado por política de red del entorno remoto (`host_not_allowed`). Briefing entregado vía commit al vault. Para restaurar la entrega por push, añade `ntfy.sh` a los hosts permitidos en la configuración de egress del entorno en https://code.claude.com/docs/en/claude-code-on-the-web.
