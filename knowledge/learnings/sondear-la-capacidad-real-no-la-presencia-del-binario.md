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
- **Sondear el COMANDO EXACTO que se va a ejecutar**, no el binario ni un subcomando barato. Sondar `docker compose version` sigue siendo insuficiente: responde con Docker vivo y el **servicio del compose parado**, y el gate muere igual (`service "postgres" is not running`). La sonda buena es el propio `docker compose exec -T <servicio> psql … 'select 1'`. Corregido en un segundo pase (#636) porque el primer arreglo repitió el fallo un escalón más abajo — **la sonda barata siempre queda un nivel por encima del fallo real**.
- **Degradar con aviso, no abortar** — si el camino alternativo ya verifica lo que el principal daba por hecho (aquí: paridad de versión cliente/servidor), degradar es seguro. Abortar deja el gate rojo por entorno, no por código.
- **Dejar un override que fuerce el camino estricto** (`DRIFT_MODE=docker`) para que un Docker roto en CI falle ruidosamente en vez de enmascararse tras la degradación.
- **Imprimir siempre el modo elegido y su motivo**, y extraer la decisión a un módulo puro para poder testearla — la de este caso no tenía ni un test.
- **Nada de puertos/hosts hardcodeados en el camino degradado**: si el resto de la conexión es env (`*_USER`/`*_PASSWORD`) y el puerto no, la máquina que ya tiene ese puerto ocupado se queda sin NINGÚN camino viable (#636 → `DRIFT_PG_PORT`).

Caso real: agh-iberica #632 → PR #633, y su residuo #636 → PR #637. Ver [[e2e-smoke-skip-honesto]] · [[docker-compose-env-not-recreate]].
