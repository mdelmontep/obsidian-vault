---
title: un claude -p que falla por la API deja el motivo en result, no en subtype
date: 2026-09-13
source: facturaia
tags: [claude-code, headless, runner, debugging]
---
Con `--output-format json`, el CLI escribe en **stdout** por qué falló y deja
stderr vacío. Pero no hay UN sitio: hay dos formas distintas y un runner que lea
solo una se queda mudo.

- **Fallo del propio CLI** (turnos agotados, ejecución): `subtype`
  (`error_max_turns`, `error_during_execution`) + `errors[]`.
- **Rechazo de la API** (auth, cuota, permisos de la org): `subtype` sigue siendo
  **`success`**, con `is_error: true`, `api_error_status: 403|401` y la causa
  **solo** en `result` — p. ej. «Your organization has disabled Claude
  subscription access for Claude Code». Exit 1 y stderr vacío.

Medir un caso (yo medí `--max-turns 1`) y generalizar deja el otro sin cubrir:
tres domingos de `last_error` = «salió con código 1». Copiar `result` es seguro
solo cuando hay `api_error_status`: sin él puede ser texto del modelo o de la web.

Para probar un token sin imprimirlo: `HOME=<tmp> CLAUDE_CODE_OAUTH_TOKEN=$(opsa
read …) claude -p 'responde solo: ok' --output-format json --max-turns 1`. La env
pisa a las credenciales del Keychain, así que la prueba mide el token que quieres.
Ver [[claude-headless-hereda-hooks-y-mcp-del-proyecto-del-cwd]].
