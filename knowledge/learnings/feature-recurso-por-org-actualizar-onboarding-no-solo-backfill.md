---
title: feature que siembra recursos por org → actualizar el onboarding de orgs nuevas, no solo backfill
date: 2026-06-01
source: claude-code-session
tags: [postgres, onboarding, mantenimiento]
---
Bug latente clásico: una feature nueva (abonos→serie B, proformas→serie F) añade una
migración que hace **backfill** del recurso a las orgs EXISTENTES, pero olvida actualizar
la función de alta de orgs NUEVAS (`handle_new_user` / RPC de onboarding / endpoint
admin). Resultado: clientes antiguos funcionan, **clientes nuevos quedan sin el recurso**
y la operación falla en prod ("Serie B no encontrada"). Pasa desapercibido porque quien
desarrolla y prueba usa una org antigua que sí lo tiene.

Fix robusto (sin tocar las funciones largas del camino crítico): **trigger AFTER INSERT
ON <tabla_org>** que crea lo que falta, idempotente (`WHERE NOT EXISTS`) → cubre todos los
caminos de alta de golpe (registro, OAuth, admin, futuros) + backfill a existentes.

Checklist al añadir feature con recursos por-org: ¿quién los crea al dar de alta una org
nueva? No basta con parchear las existentes.
