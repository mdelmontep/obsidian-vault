---
title: agentesia
date: 2026-07-22
tags: [cliente, agentesia]
---

# Agentesia (interno)

La empresa. agency-portal + ticketing chatbot + integración con TuFacturaIA + Slack canvases.

## Estado

- **agency-portal** (Borja como reviewer) — Next.js, integra con TuFacturaIA via API v1 (HMAC webhooks + outbox + Stripe-style sync)
- **`/agency/time`** — dashboard de horas del equipo (Dani/Borja/Manu): ingesta vía hooks locales de Claude Code (`ops/claude-time-tracker`), límites de uso 5h/semanal, síntesis IA (gpt-4o-mini) de qué está haciendo cada uno en "Trabajando ahora" (árbol persona→sesión, agrupado por `claudeSessionId` desde PR #166 — antes agrupaba por proyecto y fusionaba sesiones paralelas del mismo proyecto en una sola fila; la fusión de DURACIÓN sigue siendo por sesión, no se pierde)
- **Chatbot ticketing** desplegado en `89B9QN23hOHDq6oP` n8n
- **Slack workspace** activo, canvases por proyecto

## Próximos hitos

1. **agency-portal — Dani: hook time-tracker no reporta pese a reinstalar** (NOW, 22-jul) — última actividad real de Dani congelada desde hace 45+ min pese a abrir sesión nueva y escribir prompts. Se le pasaron 3 comandos de diagnóstico (config `~/.agentesia-tracker.json`, hook registrado en `~/.claude/settings.json`, test manual POST a `/api/internal/time-ingest`) — pendiente que los corra y comparta la salida (sobre todo el `HTTP_STATUS` del test manual).
2. **agency-portal — CI (Actions) bloqueado por billing, confirmado también aquí** (recurrente, mismo org que TuFacturaIA) — jobs mueren en 2-4s con "recent account payments have failed". Mismo patrón que TuFacturaIA: verificar local (`lint`+`typecheck`+`test`+`build`) antes de cada merge, `gh pr merge --merge` normal (no hace falta `--admin` aquí, a diferencia de TuFacturaIA). Ver [[github-actions-org-private-free-tier-2000-min]].
3. **agency-portal — n8n router consulta Supabase como source of truth** (NEXT, arrastrado) — TTL 30d en `aia_ob:{phone}` es tirita. Endpoint `/api/onboarding/is-active-by-phone` + nodo HTTP en `ChatBOT mejorado` antes del IF Activo + Redis a caché con re-seed. Ver [[Stack/n8n]] · [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding]]
4. **agency-portal — añadir key "manu-personal" a `TIME_TRACKER_KEYS` en Dokploy** (NEXT, 22-jul) — key ya generada (guardar en 1Password, no en el vault), falta añadirla al env y recrear el contenedor; Manu alterna `~/.agentesia-tracker.json` a mano según qué cuenta Claude use.

## Bloqueos / esperando a terceros

- Dani: correr diagnóstico del hook de time-tracker (ver hito 1)
- GitHub org: subir spending limit / esperar reset de cupo Actions (ver hito 2)
- Manu: guardar la key "manu-personal" en 1Password + actualizar `TIME_TRACKER_KEYS` en Dokploy (ver hito 4)

## Links rápidos

- [Github org](https://github.com/AgentesIA-MAdrid)
- [agency-portal](https://github.com/AgentesIA-MAdrid/agency-portal)
- Slack #pro-facturaia, #pro-agentesia
- Canvas Panel TuFacturaIA: F0AV38CHYSJ

## Histórico de hitos

- 2026-05-02: integración API v1 ↔ agency-portal viva en prod (7 PRs apilados + 7 fixes auditoría)
- 2026-06-16: onboarding WhatsApp caído — cuenta OpenAI sin saldo (`429 insufficient_quota`) → webhook 500 silencioso, bot mudo. Diagnóstico vía ejecuciones n8n. Recargado el saldo (revive sin deploy) + PR #86 para que no muera en silencio. Feature secretaría virtual HGH (PR #87) lista y validada con dry-run.
- 2026-06-22: Pizarra/board (PR #91) + secretaría virtual HGH + fixes de prefill fiscal + extracción onboarding, todo mergeado y cerrado (verificado vía `gh pr view` — el hub llevaba semanas desfasado listándolos como pendientes).
- 2026-07-22: módulo **time-tracking** completo en prod — dashboard + ingesta (#156), dominio prod correcto (#157), límites de uso 5h/semanal (#158), síntesis IA gpt-4o-mini del bloque de trabajo (#160), auto-refresco + filtros (#161), árbol "Trabajando ahora" por persona + fix de solape en cálculo de horas cuando hay sesiones concurrentes del mismo proyecto (#163). CI de Actions confirmado bloqueado por billing (mismo org que TuFacturaIA) — merges verificados en local. Ver [[merged-duration-intervalos-solapados-time-tracking]] · [[claude-code-hooks-no-se-recargan-en-sesion-abierta]].
- 2026-07-22 (tarde): **PR #165 mergeado** (Borja) — dos gráficas nuevas en `/agency/time` (técnico y proyecto) con selector estilo trading (rango/intervalo/métrica desacoplados, intervalo filtrado a 2-60 buckets legibles), coste estimado por proyecto (18,75€/h provisional), tiempo/coste **acumulado** en vez de valor puntual por bucket, leyenda propia clicable. Fix real: al agrupar por proyecto se fusionaba solape entre técnicos DISTINTOS trabajando en paralelo (topaba el bucket como si fuera 1 persona) — corregido sub-agrupando por `member` antes de fusionar. Normalizado el nombre de proyecto en el origen (`service.ts`): cada técnico lo derivaba del nombre de su carpeta local ("AGH Iberica"/"agh-iberica"/"agh_iberica" eran 3 valores), con backfill del histórico ya aplicado en BD. Ver [[metrica-topada-por-bucket-debe-mostrarse-acumulada]] · [[identificador-de-carpeta-local-diverge-entre-maquinas-normalizar-en-ingesta]] · [[merged-duration-intervalos-solapados-time-tracking]].
- 2026-07-22 (noche): **PR #166 abierto** (Manu) — "Trabajando ahora" agrupaba por `(member, project)` y fusionaba en una fila sesiones de Claude Code paralelas del mismo proyecto (Manu con varias sesiones de FacturaIA solo veía una); `buildActiveTree` ahora agrupa por `claudeSessionId`. Aparte, confirmado y arreglado el motivo de que Manu no saliera en "Límites de uso de Claude": su `statusline-command.sh` calculaba el %5h/7d pero nunca lo escribía en `~/.claude/statusline-rate-limits.json` (diagnóstico correcto de Borja, aplicado). Ver [[agrupar-vista-en-vivo-por-clave-de-negocio-colapsa-sesiones-paralelas]] · Stack `claude-code-gotchas.md`. **Pendiente identificado (no implementado)**: Manu usa 2 cuentas Claude (info + personal), cada una con cupo propio; decidido mintar un `tracker-key` nuevo para "manu-personal" en vez de tocar esquema — falta añadirlo a `TIME_TRACKER_KEYS` en Dokploy y que Manu alterne `~/.agentesia-tracker.json` a mano. Ver [[cuota-por-cuenta-externa-sin-deteccion-mint-credential-separada]].
