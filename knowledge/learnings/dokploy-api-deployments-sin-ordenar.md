---
title: "Dokploy API: compose.one devuelve deployments SIN ordenar"
date: 2026-06-12
source: facturaia falso positivo "webhook roto"
tags: [dokploy, api, gotcha]
---

`GET /api/compose.one` devuelve `deployments[]` en orden arbitrario (no por `createdAt`). Leer `deployments[0]` como "el último deploy" da falsos positivos: el 2026-06-12 concluí que el auto-deploy GitHub→Dokploy llevaba horas roto (5 commits "sin desplegar"), lancé deploy manual redundante y un commit-probe vacío — todo funcionaba; los deployments estaban más abajo en la lista.

**Siempre**: `sorted(deployments, key=lambda x: x['createdAt'])[-1]` antes de concluir nada.

Señal de contraste barata: las Recent Deliveries de la GitHub App (verde + body `"Deployed N apps"`) son la fuente de verdad de si el webhook dispara. Ojo: pueden existir apps GitHub residuales de hosts viejos con deliveries rojas (caso `Dokploy-2026-04-21` → `dokploymanu.tecnocloud.es`) que son ruido, no señal.
