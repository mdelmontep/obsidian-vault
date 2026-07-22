---
title: identificador derivado de metadata local (carpeta/hostname) diverge entre máquinas — normalizar en la ingesta
date: 2026-07-22
source: claude-code-session
tags: [data-quality, agregacion, time-tracking, agency-portal]
metadata:
  type: learning
---

Un hook local que deriva un campo (p. ej. "proyecto") del nombre de carpeta del repo (`basename(cwd)`) produce valores DISTINTOS para la misma entidad real si cada persona nombra su carpeta local distinto ("AGH Iberica" / "agh-iberica" / "agh_iberica" — 3 técnicos, 3 slugs para el mismo proyecto). Sin error visible: son datos "correctos" pero fragmentados que rompen cualquier agregación por esa clave (aparece como 3 series distintas en vez de 1).

**Fix**: normalizar (lowercase + separadores unificados a slug) en el PUNTO DE INGESTA (server, al insertar), nunca confiar en que el cliente mande el valor ya limpio, y nunca parchear con fuzzy-matching en el display. Backfill del histórico ya insertado con un UPDATE dirigido por valor exacto, tras verificar los valores reales en BD (no adivinar el mapping).

Aplica a cualquier pipeline que ingiera identificadores libres desde máquinas/usuarios distintos (hostname, carpeta, nombre de dispositivo).
