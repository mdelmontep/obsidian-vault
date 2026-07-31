---
title: op read — el secreto nunca debe aparecer literal en un comando bash, ni copiado desde memoria
date: 2026-07-04
source: claude-code-session
tags: [seguridad, 1password, credenciales, claude-code]
---
El clasificador de seguridad de Claude Code bloquea cualquier comando bash que contenga un secreto en texto plano — incluso un simple `curl` de solo lectura — si el JWT/API key aparece literal en el comando, venga de donde venga (pegado a mano, o copiado de un memory file de sesiones previas).

Fix: consumir SIEMPRE `op read "op://vault/item/campo"` inline dentro del mismo comando que lo usa (`TOKEN=$(op read ...) && curl -H "X-KEY: $TOKEN" ...`), nunca en dos pasos donde el valor quede visible en un comando intermedio o en el transcript.

Si `op` da `authorization timeout` (desktop app sin aprobar), NO caer en el atajo de usar un token guardado en memoria del agente pegándolo literal — vuelve a fallar igual, más la reautorización sigue pendiente. Pedir al usuario que reautorice 1Password antes de reintentar.

**`op read` por NOMBRE de ítem falla en silencio si el título tiene un espacio final** (31-jul, AGH). `op://Vault/Open AI AGH /credencial` da `[ERROR] … isn't an item`, pero como el valor se consume inline (`VAR=$(op read …)`), **la variable queda VACÍA y el comando sigue**. Resultado: `401 "You didn't provide an API key"` que en el scorecard salió como **`0/36` en un eje de evals** — parecía que un cambio de prompt había roto una frontera. Fix: usar el **ID del ítem** (`op item list --vault X`), estable e inmune al título. Y ante un batch que cae a cero de golpe, **verificar primero que la credencial llega** (comprobar prefijo/longitud de la variable, nunca imprimirla) antes de sospechar del código.

**Extraer/mover secretos (no solo usarlos):** al SACAR secretos de un sitio (p.ej. `docker exec <cont> env` de un Dokploy) para consolidarlos en 1Password, nunca a stdout — redirige a un fichero temporal (`> f`), `op` lo consume inline, y borra el fichero al final. Trampa: el fallback habitual cuando el clasificador bloquea un SSH read-only («que el usuario lo corra con `! comando`») **volcaría el `env` entero al transcript** → expone los secretos. Ese fallback solo vale para comandos SIN valores (un `docker ps`). Para el `env`: o autorizas el SSH y rediriges a fichero, o el usuario extrae/pega los valores él (exposición cero).

**Copiar un `.env` a un scratchpad deja la service-role en disco, y con los permisos que toque** (2026-07-25): para levantar un dev server en un worktree copié `.env.local` de otro checkout al scratchpad como respaldo. Al revisar al cerrar, uno de esos backups (de una sesión anterior) llevaba la **service-role de producción con permisos 644** — legible por cualquier proceso del sistema — llevaba ahí 16 horas. Reglas: `umask 077` antes de cualquier copia de env, `chmod 600` explícito, y **borrar sobrescribiendo (`rm -P`) al terminar, en la misma sesión que lo creó**. El scratchpad se siente efímero y no lo es. Al cerrar, barrido obligatorio: `grep -rlE "SERVICE_ROLE_KEY=ey|sk-[A-Za-z0-9]{20}|PASSWORD=." <scratchpad>` — y comprobar los permisos, no solo la existencia.
