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

## Supabase Cloud — RLS multi-tenant con SECURITY DEFINER (2026-04-19)

Patrón para SaaS multi-tenant:
1. `get_user_org_id()` SECURITY DEFINER STABLE — lee org_id de org_members via auth.uid()
2. Todas las policies: `USING (org_id = get_user_org_id())`
3. Onboarding: `create_org_for_user(org_nombre)` crea org + inserta en org_members
4. `next_invoice_number(serie)` para auto-numeración con bloqueo de fila

Ver [[rls-multi-tenant-supabase-con-security-definer]]

## AI Agent con reservas — 3 reglas anti-bug (2026-04-19)

Para cualquier AI Agent n8n que gestione reservas con Google Calendar:

1. **0 eventos = todo libre** — añadir regla explícita en prompt, Think tool y tabla de herramientas. Los LLMs interpretan lista vacía como "no disponible"
2. **Weekday number en Think** — incluir `{{ $now.weekday }}` (1-7) + fórmula + ejemplos + verificación. Sin esto el LLM calcula mal "lunes" desde "sábado"
3. **Tool description con consecuencias** — para write-tools (Reservar, Cancelar), expandir descripción a ~280 chars explicando "sin esta llamada la acción NO ocurre". Descripción genérica = LLM genera texto sin ejecutar

Ver [[google-calendar-tool-0-eventos-significa-todo-libre]], [[llm-calcula-mal-dia-semana-a-fecha-sin-weekday-number]], [[tool-description-generica-no-fuerza-ejecucion-de-tool-critica]]

---

## Kommo webhook status_lead — siempre filtrar (2026-04-20)

`status_lead` dispara en TODOS los cambios de estado, no solo el target. Añadir IF `status_id == X` después del webhook para evitar ejecuciones duplicadas. Sin esto: emails duplicados, eventos Calendar duplicados, tareas duplicadas.

Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]

## toolWorkflow onError — usar continueErrorOutput (2026-04-20)

En nodos toolWorkflow del AI Agent, `stopWorkflow` mata al agente sin respuesta al usuario. Usar siempre `continueErrorOutput`.

Ver [[toolWorkflow-onError-stopWorkflow-mata-al-agente-silenciosamente]]

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

## OCR pipeline facturas — patrón Next.js + n8n + OpenAI Vision (2026-04-20)

1. Next.js convierte archivo a base64 (`Buffer.from(arrayBuffer).toString('base64')`) — n8n Code Node sandbox no tiene `helpers.binaryToBuffer`
2. Enviar `org_nombre` en el webhook body para que el prompt distinga emisor vs receptor
3. Frontend simula progreso 0→90% con `setInterval` mientras `estado='procesando'`. Supabase Realtime sobrescribe con 100% al terminar
4. n8n actualiza `bandeja_ingesta` con PATCH directo a Supabase (no PostgREST)

Ver [[ocr-facturas-confunde-receptor-con-emisor-sin-org-nombre]], [[n8n-code-node-sandbox-no-tiene-helpers-binaryToBuffer]]

## Dokploy — Traefik reload obligatorio tras redeploy (2026-04-20)

Cada redeploy deja Bad Gateway. Contenedor arranca OK pero Traefik no re-descubre la ruta.
**Fix**: Dokploy → Settings → Web Server → Reload. Verificar contenedor con `ps aux` + `netstat -tlnp` antes.

Ver [[dokploy-requiere-reload-manual-traefik-tras-redeploy]]

## n8n $if isExecuted para ramas IF (2026-04-20)

En workflows con ramas condicionales, cualquier expresión que referencia un nodo de otra rama debe usar:

```
={{ $if($('Nodo').isExecuted, $('Nodo').item.json.campo, fallbackValue) }}
```

Sin esto: error silencioso que rompe la ejecución. Caso típico: contacto existente vs nuevo, cada uno crea por su rama pero un nodo posterior referencia solo una.

Ver [[n8n-expresion-nodo-no-ejecutado-falla-silencioso]]

## Calendar events formato limpio (2026-04-20)

Para Clínica Zen (y cualquier proyecto con Calendar):
- **Summary**: `Valoración - Odontología - Ana López` (legible en vista calendario)
- **Description**: Lead ID, teléfono, email, motivo, fuente (datos para gestión)

Google Calendar `query` busca en summary + description, así que poner Lead ID en description funciona para buscar/cancelar/mover eventos programáticamente.

---

## FacturaIA — pdf-lib para generar PDFs server-side (2026-04-20)

PDFKit falla en Turbopack (ENOENT .afm). Usar pdf-lib: `PDFDocument.create()` + `StandardFonts`.
Seed: nunca insertar campos calculados (facturado, pendiente, gasto) — columnas no existen en BD.
API routes internas sin sesión: header `x-service-key` con service_role key.

Ver [[pdf-lib-funciona-en-nextjs-turbopack-donde-pdfkit-falla]], [[supabase-insert-silencioso-con-ts-nocheck-oculta-columnas-inexistentes]]

## Conciliación bancaria IA — patrón prompt 2 fases (2026-04-21)

Pipeline para cruzar extractos bancarios con facturas:
1. Fase 1 (extracción): Claude parsea cualquier formato → JSON de movimientos
2. Fase 2 (matching): Claude recibe movimientos + facturas pendientes + reglas aprendidas → matches con score
- Prompt caching: facturas/reglas en bloque cached, solo movimientos dinámicos
- Scoring con tabla numérica fija (+50 importe, +25 nombre, +15 fecha, -100 descarte)
- Comparar siempre contra factura.total (con IVA), nunca base
- Hash dedup: cuenta+fecha+concepto+importe+idx (idx evita falsos positivos)
- Batches de 50 si >100 movimientos
- Umbral auto-aprobación: 95 para gestorías, configurable por org

Ver spec: `facturaia/docs/superpowers/specs/2026-04-21-conciliacion-bancaria-design.md`

---

## Obsidian vault sync via GitHub (2026-04-18)

Vault en `/Users/manueldelmonte/Obsidian/Manu/` sincronizado con `mdelmontep/obsidian-vault` (privado).
`/obsidian-1` hace push automático al final. Daily Briefing Manu lee de ahí cada mañana L-V 9:00.
Trigger ID: `trig_01THsqqvV3pg3WNnbgvkkdzk`
