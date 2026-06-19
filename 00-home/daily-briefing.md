---
title: daily briefing
date: 2026-06-19
tags: [home, briefing]
---

# 🌅 Briefing 19-jun

## ✅ Lo que cerraste ayer

**Panel de feedback rediseñado en TuFacturaIA**

Has rehecho el módulo de soporte para que desde una sola pantalla puedas responder al cliente, dejar una nota interna para el equipo o darle instrucciones a Claude — con un selector explícito que deja claro a dónde va cada mensaje. Antes era un campo de texto sin contexto; ahora el hilo muestra etiquetas de destino y las acciones de estado (resolver, descartar, reabrir) son siempre visibles.

**Cómo lo usas en la práctica**:
- Cuando llega un ticket de una factura errónea, escribes la causa técnica como nota interna y la respuesta al cliente en el mismo flujo, sin cambiar de pantalla.
- Si quieres que Claude retome un ticket complejo, le mandas la instrucción directamente desde el panel sin copiar contexto.
- "Marcar resuelto", "Descartar" y "Reabrir" siempre visibles — sin buscar en menús.

**Auditoría de rendimiento de BD + limpieza de logs (PR #375)**

Has añadido los índices que faltaban en las tablas más consultadas (`lineas_factura`, `bandeja_ingesta`), paginado el listado de orgs en admin (que antes cargaba todo el JSONB de settings de golpe) y creado un cron que purga automáticamente los logs de API y cron de más de 90 días. Todo en producción.

**Cómo lo usas en la práctica**:
- El panel `/admin/orgs` carga ahora en milisegundos aunque haya cientos de organizaciones.
- Los logs dejan de crecer sin control — en 3 meses la BD habrá purgado la acumulación histórica.

## 🎯 Hoy en orden de prioridad

1. **Notificaciones fiscales residuales (TuFacturaIA)** — Marcar leídas las notifs viejas y recalcular los borradores 130 del 2T/3T/4T (drift real: abono B2026-0001). Revisar visualmente el drawer: X 28px y fade de chips. Trabajo manual, ~30 min.
2. **Centro Elphis — go-live** — El único bloqueo real es el host IMAP y la contraseña de `info@centroelphis.com`. Sin eso el sync de email no arranca y el go-live está parado. Hacer seguimiento a Pablo/Alba hoy.
3. **agency-portal — smokes PRs #72/#73/#75/#77/#78** — Cinco verificaciones tras merge: extracción onboarding por sección, factura prerellena con datos fiscales del cliente y facturas directas FacturaIA en portal con PDF descargable.

## ⏳ Pendientes y bloqueos

- **Esperando a Pablo/Alba (Elphis)**: host IMAP + contraseña `info@centroelphis.com` (bloqueado varios días)
- **Acción Manu — OpenAI Tier 2**: bot WhatsApp en rate-limit 30k TPM. Subir en platform.openai.com → settings → limits.
- **Acción Manu — GitHub Actions billing**: CI muerto desde 17/06 ~13:00 por límite de gasto. Arreglar pago en Settings → Billing org `AgentesIA-MAdrid`.

## 💡 Quick win sugerido

**Corregir ID receptor obsoleto en `CLAUDE.md`** — Una sola línea: cambiar `zYcHHa8jWXB6dY5i` por `pqSWkDIHqmSVHotB` en la tabla de routing. 5 minutos y ningún agente futuro apuntará a un workflow que da 404.

## ⚠️ Stale (>7 días)

- **IET deploy a iet.es**: web lista en `iet-preview.surge.sh` desde hace semanas. Solo falta subir `dist/` por FTP a Apache. Empujar o pedir fecha concreta al cliente.
- **Ticket bgchivite `1762f07e`**: el fix de rendimiento (#209) lleva días en prod. Solo queda responder. 5 minutos.
