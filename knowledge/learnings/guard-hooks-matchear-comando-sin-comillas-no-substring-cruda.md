---
title: hooks-guard de comandos — matchea sobre el comando SIN comillas, no substring cruda (falso positivo en --body/-m)
date: 2026-07-14
source: claude-code-session
tags: [claude-code, hooks, git, seguridad]
---
Un PreToolUse(Bash) que bloquea comandos peligrosos (git-guard: `reset --hard`, `push --force`, commit en main…) NO debe matchear por **substring sobre todo el comando**: un comando benigno cuyo *texto de argumento* menciona la frase da FALSO POSITIVO. Casos reales que se bloquearon solos: `gh pr create --body "… reset --hard …"` y `git commit -m "… push --force …"` (¡y me bloqueó mi propio `gh pr create` describiendo el fix!).

Fix: antes de matchear, **quita el contenido entre comillas** (un git peligroso real nunca va entre comillas):
```sh
scrubbed=$(printf '%s' "$cmd" | sed -e 's/"[^"]*"//g' -e "s/'[^']*'//g")
```
y corre TODOS los greps/case sobre `$scrubbed`. Solo hace el guard MÁS permisivo (ignora texto de args), nunca más débil ante un peligro real (que va sin comillas). Verifícalo con: FP entre comillas pasa · peligro real bloquea · `--force-with-lease` pasa.

Ojo: hay dos hooks con este patrón — el del repo (`.claude/hooks/`) y el global (`~/.claude/hooks/`); arregla LOS DOS. Ver [[subagente-feature-sin-cablear-composicion]] (verificar el efecto real, no solo el código).

Corolario (2026-07-17, hook que ENRUTA en vez de bloquear, [[fia-gate]]): para decidir "esto es un build de verdad" y no una mención en `git commit -m "…build…"` / `grep` / `echo`, quitar comillas se queda corto. Ancla a POSICIÓN de comando: trocea por `&&`/`||`/`;`/`|`/`&`, quita asignaciones de entorno del inicio (`FOO=bar `) y exige que el segmento EMPIECE por el objetivo (`^npm run build`). Así `cd x && npm run build` sí matchea y `echo "npm run build"` no.

Corolario 2 (2026-08-18) — **dos COTAS del mecanismo, no del patrón**, medidas en agh-iberica:

1. **El hook recibe la cadena tal como se escribió, nunca los valores expandidos.** Mismo comando:
   `git push origin --delete <rama-literal>` → BLOQUEADO; `B=<rama>; … --delete "$B"` → PASA. Así que
   toda regla que case contra un **argumento** se esquiva metiéndolo en una variable, y sin intención:
   un bucle que borra 14 ramas pasó 14 veces y la 15ª, a mano, se bloqueó. Robusto es lo que depende de
   la **forma del verbo** y de flags literales. Si una regla depende de un argumento: o se declara
   best-effort **en el mensaje del hook**, o se mueve a un `pre-push` de git, que sí recibe los refs.
2. **El hook del repo vive DENTRO del árbol que vigila** (`$CLAUDE_PROJECT_DIR/.claude/hooks/…`), así
   que un checkout atrasado ejecuta **su** versión: se midió 50 líneas con una regla ya borrada contra
   88 en `main`. O sea **corrección mergeada y NO activa**, con la PR y el issue cerrados. Y forma
   DEADLOCK con la guarda de «checkout compartido»: el único remedio —adelantar el árbol— usa el verbo
   de fusión, y la condición `worktrees > 1` incluye el raíz, así que tampoco se sale retirando
   worktrees. 👉 *La activación de la corrección requería la corrección*, y el hook viejo llegó a
   bloquear el comando que lo arreglaba.
   Fix aplicado en los DOS hooks: eximir el **fast-forward puro al remoto rastreado** (no crea commit,
   no puede divergir porque iguala, no pisa trabajo sin commitear, no mueve el HEAD de los worktrees),
   con el destino **exacto** exigido y **borrando el segmento exento para aplicar la regla al RESTO** —
   así un compuesto con algo detrás sigue bloqueándose. Más un **aviso** (no bloqueo) si la copia no es
   la de `main`: delegar en la de `main` haría imposible desarrollar el propio hook.

Corolario 3 (2026-08-23) — **anclar a posición no basta si el regex del verbo es frágil**. El filtro
`^git( -[^ ]+)* commit\b` de `mutate-guard` se saltaba con **once** formas, todas `exit 0` con
código+test y sin víctima, y ninguna cubierta por test: `git  commit` (**dos espacios**),
`git<TAB>commit`, `FOO=1 git commit`, `command`/`eval`/`timeout`/`\git`, `git -C . commit`,
`git -c user.name=a commit` (opción global **con argumento separado**: rompe el `( -[^ ]+)*` porque el
token siguiente no empieza por `-`) y `git --no-pager commit`. Un espacio de más lo apagaba. Normaliza
(espacios y tabs colapsados, prefijos de entorno y envoltorios pelados) y compara el subcomando por
**token exacto** — ojo, eso hace que `git commit-tree` deje de disparar, que es correcto pero es un
cambio de comportamiento con su test.

Y dos cotas del mecanismo que salieron al arreglarlo:
- **Tokenizar cuesta, y lo paga cada llamada.** Un `sed` por segmento con `sed` partiendo por líneas dio
  **1.299 ms** en un heredoc de 500 líneas (`cat > f <<'PY'`, el gesto de escribir un fichero) contra
  14 ms del hook viejo. Es `PreToolUse(Bash)`: se paga en TODAS las llamadas, no en los commits. Fix:
  pre-filtro barato antes del bucle (si el comando no contiene la cadena del verbo, salir) — quedó por
  debajo del original, 8 vs 9 ms.
- **Saltar el cuerpo de un heredoc no es perf, es cierre de un bypass**: un `cd` escrito DENTRO del
  fichero que se está creando movía la medición a otro repo.

Ver [[rebase-continue-estripa-las-lineas-del-mensaje-que-empiezan-por-almohadilla]] ·
[[un-remedio-corrido-desde-un-checkout-viejo-repara-a-la-version-vieja]]
