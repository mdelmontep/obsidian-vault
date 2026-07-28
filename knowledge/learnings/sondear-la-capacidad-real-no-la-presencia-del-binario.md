---
title: detectar una dependencia externa sondeando el binario, no la capacidad, elige el camino roto
date: 2026-07-28
source: claude-code-session
tags: [infra, docker, testing, gate, deteccion-de-entorno]
---
Un script que decide entre dos caminos (con dependencia / sin ella) suele detectar así:

```ts
try { execFileSync("docker", ["--version"], {stdio:"ignore"}); return true } catch { return false }
```

Eso comprueba que **el binario existe**, no que la capacidad **funcione**. Con Docker Desktop *parado*, o un shim de podman/colima en el PATH, devuelve `true` → se elige el camino Docker → muere en la primera llamada real con un error que no menciona Docker ni la salida (`unknown shorthand flag: 'T' in -T`, exit 125).

**El caso probable es el que rompe**: "instalado pero apagado" es mucho más común que "ausente", y es justo el que la sonda no cubre.

Reglas:
- **Sondear el subcomando que de verdad se va a usar** (`docker compose version`), no el binario ni `--version`.
- **Degradar con aviso, no abortar** — si el camino alternativo ya verifica lo que el principal daba por hecho (aquí: paridad de versión cliente/servidor), degradar es seguro. Abortar deja el gate rojo por entorno, no por código.
- **Dejar un override que fuerce el camino estricto** (`DRIFT_MODE=docker`) para que un Docker roto en CI falle ruidosamente en vez de enmascararse tras la degradación.
- **Imprimir siempre el modo elegido y su motivo**, y extraer la decisión a un módulo puro para poder testearla — la de este caso no tenía ni un test.

Caso real: agh-iberica #632 → PR #633. Ver [[e2e-smoke-skip-honesto]] · [[docker-compose-env-not-recreate]].
