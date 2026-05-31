---
title: dokploy api compose.one — las env viven en composeFile, no en el campo env
date: 2026-05-31
source: claude-code-session
tags: [dokploy, infra, diagnostico, env]
---

Al diagnosticar una env var de un stack tipo **compose** vía `GET /api/compose.one?composeId=`, el campo `env` de la respuesta suele venir **vacío**: las variables están inline en el campo **`composeFile`** (el YAML docker-compose). Parsear solo `env` da falsos "AUSENTE"/"0 vars" aunque la app funcione perfectamente.

Síntoma real (2026-05-31, TuFacturaIA): `FACTURAIA_SERVICE_KEY presente: False` + `SUPABASE: False` + `total vars: 0` → imposible si la app prod arranca. Pista: si una key conocida (SUPABASE) sale ausente, **estás mirando el campo equivocado**.

Fix: buscar en `composeFile` (o concatenar `composeFile + env`). Estructura de respuesta puede ser `d['data']` o `d['result']['data']` — usar acceso robusto `(d.get('result',{}).get('data') or d.get('data') or d)`.

Aún así, el valor en `composeFile` puede tener interpolación `${VAR}`. La **única fuente de verdad del runtime** es `docker exec <container> printenv VAR` (SSH) o el panel Dokploy → Environment. No afirmar "ausente/mismatch" desde la API sin confirmar runtime.

Relacionado: verificar el **síntoma** (activar workflow y mirar ejecución) antes de perseguir hipótesis de config — el "mismatch de key" resultó falso, solo faltaba activar el workflow n8n.
