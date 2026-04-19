---
title: hot cache
date: 2026-04-17
tags: [stack, index]
---

# Hot Cache — Últimas 2 semanas

Patrones y soluciones recientes que probablemente se reutilicen pronto.
Se lee PRIMERO antes de buscar en el resto del vault.

> Si algo tiene más de 2 semanas aquí, moverlo al índice correspondiente en Stack/ o eliminarlo.

---

## AI Agent con reservas — 3 reglas anti-bug (2026-04-19)

Para cualquier AI Agent n8n que gestione reservas con Google Calendar:

1. **0 eventos = todo libre** — añadir regla explícita en prompt, Think tool y tabla de herramientas. Los LLMs interpretan lista vacía como "no disponible"
2. **Weekday number en Think** — incluir `{{ $now.weekday }}` (1-7) + fórmula + ejemplos + verificación. Sin esto el LLM calcula mal "lunes" desde "sábado"
3. **Tool description con consecuencias** — para write-tools (Reservar, Cancelar), expandir descripción a ~280 chars explicando "sin esta llamada la acción NO ocurre". Descripción genérica = LLM genera texto sin ejecutar

Ver [[google-calendar-tool-0-eventos-significa-todo-libre]], [[llm-calcula-mal-dia-semana-a-fecha-sin-weekday-number]], [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]]

---

## Retell → n8n checklist (2026-04-18)

Antes de subir un prompt de Retell que conecta con webhooks de n8n:

1. URLs de tools apuntan al dominio correcto (`dig +short` para verificar — EasyPanel ≠ dominio custom)
2. Cada tool referenciada en el prompt existe en `general_tools`
3. Nombres de parámetros coinciden con `Edit Fields` / `Set` del workflow n8n
4. Workflow destino activo y no archivado
5. `parameter_type: "json"` si n8n espera `body.args.X`

Ver [[retell-parameter-type-form-vs-json-rompe-n8n-silenciosamente]] y [[easypanel-y-dominio-custom-pueden-resolver-a-ips-distintas]]

## Slack API — escribir en canvas (2026-04-18)

```bash
# 1. Unir bot al canal
curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"channel":"C0ARS4X5MF0"}' "https://slack.com/api/conversations.join"

# 2. Editar canvas (insert al final)
curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{"canvas_id":"F0AT6KEJLQZ","changes":[{"operation":"insert_at_end","document_content":{"type":"markdown","markdown":"- [ ] Tarea nueva\n"}}]}' \
  "https://slack.com/api/canvases.edit"
```

- Canvas Tareas Pendientes: file_id `F0AT6KEJLQZ` en canal `C0ARS4X5MF0` (#01-tareas-pendientes)
- Bot no tiene `groups:read` — solo listar canales publicos
- Ver [[slack-canvas-api-requiere-changes-array-con-operation]] y [[slack-bot-sin-groups-read-no-lista-canales-privados]]

## n8n API — credenciales no expuestas (2026-04-18)

`GET /api/v1/credentials` lista id/nombre/tipo pero nunca devuelve secrets. Guardar tokens fuera de n8n si se necesitan en otro contexto.
Ver [[n8n-api-publica-no-expone-valores-de-credenciales]]

## Migración masiva de workflows n8n vía script Python (2026-04-18)

Patrón para resetear N workflows desde JSONs originales con reemplazo de IDs:

1. Script Python lee JSONs originales + aplica `str.replace()` por cada par viejo→nuevo (credenciales, field_ids, pipeline, status, sub-workflow IDs, dominios, etc.)
2. Extrae solo campos válidos para la API: `name`, `nodes`, `connections`, `settings`, `staticData`
3. Guarda en `/tmp/cz_upload/` → sube con `PUT /api/v1/workflows/{id}`
4. Activar después con `POST /api/v1/workflows/{id}/activate`

Clave: los `field_id` en Code nodes van SIN comillas (`field_id: 337714`), necesitan reemplazo por separado de los que van como string.

Ver [[kommo-llt-requiere-subdominio-cuenta-no-api-c]] y [[n8n-debounce-redis-1s-causa-duplicados-en-chatbot]]

## Obsidian vault sync via GitHub (2026-04-18)

Vault en `/Users/manueldelmonte/Obsidian/Manu/` sincronizado con `AgentesIAMadrid/obsidian-vault` (público).
`/obsidian-1` hace push automático al final. Daily Briefing Manu lee de ahí cada mañana L-V 9:00.
Trigger ID: `trig_01THsqqvV3pg3WNnbgvkkdzk`
