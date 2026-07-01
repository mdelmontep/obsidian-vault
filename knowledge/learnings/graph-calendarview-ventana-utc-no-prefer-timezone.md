---
title: graph calendarview interpreta la ventana en utc, no por prefer:outlook.timezone
date: 2026-07-02
source: claude-code-session
tags: [microsoft-graph, m365, timezone, calendar]
---

En Microsoft Graph `GET /me/calendarView`, los `startDateTime`/`endDateTime` se interpretan
por el **offset incluido en el propio valor**; si no lleva offset → se interpretan como **UTC**.
El header `Prefer: outlook.timezone="…"` **solo cambia la zona en que se renderiza la respuesta**,
NO la ventana consultada (verificado contra doc oficial).

Efecto: pedir "hoy" como `2026-07-02T00:00:00`/`...T23:59:59` (naive) consulta 00:00–23:59 UTC
= 02:00 Madrid hoy → 01:59 Madrid mañana (verano). Se pierden reuniones de 00:00–02:00 de hoy.

Fix: incluir el offset real de la TZ para esa fecha (Intl `DateTimeFormat` con
`timeZoneName:'longOffset'` → "GMT+02:00", respeta DST) y usar ventana **half-open**
`[hoy T00:00±offset, mañana T00:00±offset)`. Mantener el `Prefer` solo para el render.
