---
title: chatwoot labels post reemplaza todos — get + merge antes de añadir
date: 2026-06-04
source: claude-code-session
tags: [chatwoot, labels, api]
---
`POST /api/v1/accounts/{id}/conversations/{conv}/labels` con `{"labels":["nuevo"]}`
REEMPLAZA todos los labels existentes, no añade.
Para añadir sin borrar:
1. `GET /conversations/{conv}/labels` → `payload` (array de strings)
2. Merge: `[...new Set([...existing, ...nuevos])]`
3. `POST` con el array merged
Sin el GET, añadir "atencion-humana" borra "cita-confirmada" que ya estaba.
Aplica también en webhooks n8n donde se setean labels de forma reactiva por turno.
