---
title: daily briefing
date: 2026-06-21
tags: [home, briefing]
---

# 🌅 Briefing 21-jun

## ✅ Lo que cerraste ayer

**Paginación en toda la app de TuFacturaIA**

Has añadido paginación real desde el servidor en las 7 vistas principales: facturas, presupuestos, clientes, inventario, conciliación, ingesta y auditoría. Antes todas cargaban todos los registros de golpe — ahora cada listado devuelve solo la página que toca. Con cuentas que acumulan cientos de registros, la diferencia al abrir cualquier tabla es inmediata.

**Cómo lo usas en la práctica**:
- Cuando un cliente con 300 facturas abre `/emitidas`, la pantalla aparece al instante en vez de esperar a que lleguen 300 filas.
- Desde el inventario puedes añadir un ajuste directo por fila sin salir de la lista.
- Conciliación, ingesta y auditoría usan la misma barra de paginación — coherente en toda la app.

Además: arreglado un bug que provocaba logout inesperado en el MCP cuando el servidor de tokens tardaba y el cliente reintentaba (doble submit), y corregido el nombre legal en los XML de VeriFactu a `AgentesiaLab S.L.` (el NIF del productor ya no salía vacío en prod).

## 🎯 Hoy en orden de prioridad

1. **Notifs fiscal residuales (TuFacturaIA)** — Marcar leídas las notifs viejas y recalcular borradores 130 del 2T/3T/4T. Revisar visualmente el drawer (X 28px, fade chips). ~30 min.
2. **Centro Elphis — go-live** — El único bloqueo real sigue siendo el IMAP de `info@centroelphis.com`. Presionar a Pablo/Alba hoy o el go-live no sale.
3. **agency-portal — smoke PR #67** — Confirmar que "Progreso por sección" y "Respuestas extraídas" se rellenan tras cada turno. Si aparece `onboarding.extraction_failed`, abrir issue.

## ⏳ Pendientes y bloqueos

- **Esperando a Pablo/Alba (Elphis)**: host IMAP + contraseña `info@centroelphis.com` (bloqueado varios días)
- **Acción Manu — GitHub Actions billing**: CI muerto desde 17/06. Arreglar pago en Settings → Billing org `AgentesIA-MAdrid`.
- **Acción Manu — OpenAI Tier 2**: bot WhatsApp en rate-limit 30k TPM. Subir en platform.openai.com → settings → limits.

## 💡 Quick win sugerido

**`bancario_umbral_anomalia` en el catálogo de settings** — Una línea en `catalog.ts` (~línea 258). Sin esto el cron usa el umbral de anomalía hardcodeado en vez del configurable por org. 5 minutos.

## ⚠️ Stale (>7 días)

- **IET deploy a iet.es**: web lista en `iet-preview.surge.sh` desde hace semanas. Solo falta FTP. Empujar o pedir fecha concreta al cliente.
- **Ticket bgchivite `1762f07e`**: fix #209 lleva días en prod. Solo queda responder. 5 minutos.
